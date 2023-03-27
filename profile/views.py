from django.shortcuts import render, HttpResponse

def login_page(request):
    return render(request, 'login.html')
def logout_page(request):
    return render(request, 'logout.html')

def signup_view(request):
    return render(request, "signup.html")

def profile_view(request):
    return render(request, "profile.html")
