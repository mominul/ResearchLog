from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from profile.models import Profile
from django.contrib import messages
from .tokens import generate_tokens
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from ResearchLog import settings

def login_page(request):
    
    if not request.user.is_authenticated:      
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['psw']
            
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, "Incorrect password!")
            else:
                messages.error(request, "Unknown email, please signup first!")
                return redirect('/login')

        return render(request, 'login.html')
    
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'logout.html')

def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            # Use the email's username
            username = email.split('@')[0]
            password1 = request.POST['psw']
            password2 = request.POST['psw-repeat']

            if not email.endswith("@uap-bd.edu"):
                messages.error(request, "Only valid uap-bd.edu accounts are accepted!")
                return redirect('/signup')
            
            if User.objects.filter(email=email):
                messages.error(request, "Emali already registered!")
                return redirect('/signup')
                        
            if password1 != password2:
                messages.error(request, "Password didn't match!")
                return redirect('/signup')

            newuser = User.objects.create_user(username, email, password1, first_name=fname, last_name=lname)
            newuser.is_active = False
            newuser.save()

            messages.success(request, "Your Account has been successfully created. We have a confirmation email, please confirm your email in order to activate your account.")

            current_site = get_current_site(request)
            email_subject = "Confirm your email"
            email_body = render_to_string('email_confirmation.html', {
                'name': f'{fname} {lname}',
                'domain': current_site.domain,
                'uid': newuser.pk, 
                'token': generate_tokens.make_token(newuser)
            })

            email =  EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [newuser.email],
                
            )
            email.fail_silently=True
            email.send()

            return redirect('/')
    return render(request, "signup.html")

def activate(request, uid, token):

    try:
        newuser = User.objects.get(pk=uid)
       
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        newuser = None
        
    if newuser is not None and generate_tokens.check_token(newuser, token):
        newuser.is_active=True 
        newuser.save()
        messages.success(request,'Account activated successfully!')
        login(request, newuser)
        return  redirect('/')
    else:
        return render(request,'activation_failed.html')

def forgot_password(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            email=request.POST['email']
            forgot_user=User.objects.filter(email=email).exists()
            if forgot_user:

                forgot_user_object=User.objects.get(email=email)
                current_site = get_current_site(request)
                email_subject = "Forgot Password"
                email_body = render_to_string('email_forgot_password.html', {
                    'name': forgot_user_object.username,
                    'domain': current_site.domain,
                    'uid': forgot_user_object.pk, 
                    'token': generate_tokens.make_token(forgot_user_object)
                }
                )
                email =  EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [forgot_user_object.email],
                    
                )
                email.fail_silently=True
                email.send()
            messages.success(request,'Email sent successfully')
            return redirect('/login')
        return render(request,'forgot_password.html')
    else:
        return redirect('/')

def forgot_password_active_url(request,uid,token):
    try:
        resetuser = User.objects.get(pk=uid)
       
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        resetuser = None
    
    if resetuser is not None and generate_tokens.check_token(resetuser, token):
       return  render(request, 'reset_password.html',{'uid': uid})
    else:
        return render(request,'activation_failed.html')
    
def reset_password(request):
    if request.method=='POST':
        uid=request.POST['uid']
        password1=request.POST['psw']
        password2=request.POST['psw-repeat']

        try:
            resetuser = User.objects.get(pk=uid)
       
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            resetuser = None
        if resetuser is not None:

            if password1 != password2:
                    messages.error(request,"Password didn't match!")
                    return  render(request, 'reset_password.html',{'uid': uid})
            resetuser.set_password(password1)
            resetuser.save()
            messages.success(request,'Your password has been successfully updated')
    return redirect('/login')

def profile_update_view(request):
    data = {}
    if request.user.is_authenticated:      
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            desc = request.POST['desc']
            scholar_id = request.POST['scholar_id']
            gh_id = request.POST['gh_id']
            profile_pic = request.FILES['profile_pic']
            profile = None

            if Profile.objects.filter(user_id= request.user.id):
                profile = Profile.objects.get(user_id= request.user.id)
            else:
                profile = Profile(user_id = request.user.id)
            
            user = request.user
            user.first_name = fname
            user.last_name = lname
            profile.description = desc
            profile.gh_id = gh_id
            profile.scholar_id = scholar_id
            profile.profile_pic = profile_pic
            profile.save()
            user.save()
            print("Saved!")
            return redirect(f'/profile/{user.id}')
        else:
            profile = None
            user = User.objects.get(id=request.user.id)
            print(user)

            if Profile.objects.filter(user= request.user.pk):
                profile = Profile.objects.get(user= request.user)
            else:
                profile = Profile()
                print("not found")

            data = {
                'name': user.first_name + ' ' + user.last_name,
                'fname': user.first_name,
                'lname': user.last_name,
                'desc': profile.description,
                'scholar_id': profile.scholar_id,
                'gh_id': profile.gh_id,
                'profile_pic' : profile.profile_pic
            }
    
    return render(request, "profile_user.html", data)

def profile_view(request, id):
    profile = None
    user = User.objects.get(id=id)

    # Only the logged in user can update his profile
    can_update = id == request.user.id
    
    if Profile.objects.filter(user=id):
        profile = Profile.objects.get(user=user)
    else:
        profile = Profile()
        print("not found")
    
    pub_list = []
    
    for pub in user.publication_set.all():
        users=[]
        categories = []

        for c in pub.category.all():
            categories.append(c.category)

        for j in pub.authors.all():
            users.append({
                "name": f"{j.first_name} {j.last_name}",
                "id": j.id
            })
        
        dict = {
            "id": pub.pk,
            "authors":users,
            "title":pub.title,
            "desc": pub.description,
            "categories": categories,
            "image": pub.front_pic.url,
        }
        pub_list.append(dict)

    data = {
        'can_update': can_update,
        'name': user.first_name + ' ' + user.last_name,
        'fname': user.first_name,
        'lname': user.last_name,
        'desc': profile.description,
        'email': user.email,
        'scholar_id': profile.scholar_id,
        'gh_id': profile.gh_id,
        'profile_pic': profile.profile_pic,
        'publications': pub_list,
    }

    return render(request, 'profile.html', data)
