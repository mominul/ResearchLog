from django.shortcuts import render, HttpResponse

def login_page(request):
    return (render, 'login.html')
def logout_page(request):
    return (render, 'logout.html')