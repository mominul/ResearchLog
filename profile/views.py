from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def login_page(request):
    if not request.user.is_authenticated:      
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['psw']
            print(email, password)

            user = authenticate(email=email, password=password)
            print(user)

            if User.objects.filter(email=email):
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    print("LogIn Successfull")
                    return redirect('/')
            else:
                print("username or password maybe incorrect")
                return redirect('/login')

        return render(request, "login.html")
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
            username = fname + '_' + lname
            email = request.POST['email']
            password1 = request.POST['psw']
            password2 = request.POST['psw-repeat']
            
            if User.objects.filter(email=email):
                print("Emali already registered!")
                return redirect('/signup')
                        
            if password1 != password2:
                print("Password didn't match!")
                return redirect('/signup')

            newuser = User.objects.create_user(username, email, password1)
            newuser.save()
            return redirect('/')
    return render(request, "signup.html")

def profile_view(request):
    return render(request, "profile.html")
