from django.shortcuts import render, HttpResponse
from journals.models import Category
from django.contrib.auth.models import User

def home_view(request):
    category = []
    for cat in Category.objects.all():
        category.append(cat.category)
    
    user = User.objects.get(id=request.user.pk)
    published = len(user.publication_set.filter(is_approved=True))
    awaiting = len(user.publication_set.filter(is_approved=False))

    data = {
        "category": category,
        "pub_count": published,
        "awaiting": awaiting,
    }

    return render(request, 'home.html', data)
