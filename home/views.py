from django.shortcuts import render, HttpResponse
from journals.models import Category

def home_view(request):
    category = []
    for cat in Category.objects.all():
        category.append(cat.category)

    data = {
        "category": category,
    }

    return render(request, 'home.html', data)
