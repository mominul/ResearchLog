from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User

def login_page(request):
    return render(request, 'login.html')
def logout_page(request):
    return render(request, 'logout.html')

def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['psw']
            password2 = request.POST['psw-repeat']
            
            if User.objects.filter(username=username):
                #messages.error(request, "Username already exist! please try some other username")
                print("Username already exist! please try some other username")
                return redirect('/signup')
            
            if User.objects.filter(email=email):
                # messages.error(request, "Emali already registered!")
                print("Emali already registered!")
                return redirect('/signup')
                        
            if password1 != password2:
                # messages.error(request,"Password didn't match!")
                print("Password didn't match!")
                return redirect('/signup')
            
            if not username.isalnum():
                # messages.error(request,"Username must be Alpha-Numeric!")
                print("Username must be Alpha-Numeric!")
                return redirect('/signup')


            newuser = User.objects.create_user(username, email, password1)
            # newuser.is_active=False
            newuser.save()
    return render(request, "signup.html")

def profile_view(request):
    return render(request, "profile.html")
