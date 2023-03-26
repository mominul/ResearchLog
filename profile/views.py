from django.shortcuts import render, HttpResponse

def login_page(request):
    return render(request, 'login.html')
def logout_page(request):
    return render(request, 'logout.html')