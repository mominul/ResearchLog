from django.shortcuts import render, HttpResponse

def home_view(request):
    # return HttpResponse("<h1>Hi</h1>")
    return render(request, 'home.html')
