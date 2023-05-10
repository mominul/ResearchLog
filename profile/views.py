from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from profile.models import Profile
from django.contrib import messages
from journals.models import Publication,Authorship

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
            
            if User.objects.filter(email=email):
                messages.error(request, "Emali already registered!")
                return redirect('/signup')
                        
            if password1 != password2:
                messages.error(request, "Password didn't match!")
                return redirect('/signup')

            newuser = User.objects.create_user(username, email, password1, first_name=fname, last_name=lname)
            newuser.save()
            return redirect('/')
    return render(request, "signup.html")

def profile_update_view(request):
    data = {}
    if request.user.is_authenticated:      
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            desc = request.POST['desc']
            scholar_id = request.POST['scholar_id']
            gh_id = request.POST['gh_id']
            
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
            }
    
    return render(request, "profile_user.html", data)

def profile_view(request, id):
    profile = None
    user = User.objects.get(id=id)
    author=Authorship.objects.filter(user=user)
    # Only the logged in user can update his profile
    can_update = id == request.user.id
    
    if Profile.objects.filter(user=id):
        profile = Profile.objects.get(user=user)
    else:
        profile = Profile()
        print("not found")

    data = {
        'can_update': can_update,
        'name': user.first_name + ' ' + user.last_name,
        'fname': user.first_name,
        'lname': user.last_name,
        'desc': profile.description,
        'email': user.email,
        'scholar_id': profile.scholar_id,
        'gh_id': profile.gh_id,
        'authors':author,
    }

    return render(request, 'profile.html', data)
