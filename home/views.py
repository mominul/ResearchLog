from django.shortcuts import render, HttpResponse
from journals.models import Category
from django.contrib.auth.models import User
from profile.models import Profile
from django.contrib.staticfiles import finders
from django.templatetags.static import static

def home_view(request):
    category = []
    published = None
    awaiting = None

    for cat in Category.objects.all():
        category.append(cat.category)
    
    if request.user.is_authenticated and not request.user.is_staff:
        user = User.objects.get(id=request.user.pk)
        published = len(user.publication_set.filter(is_approved=True))
        awaiting = len(user.publication_set.filter(is_approved=False))

    users = []
    
    # Top 5 authors
    top_users = list(User.objects.filter(is_staff=False))[:6]

    def sort(i):
        l = len(i.publication_set.filter(is_approved=True))
        return l

    top_users.sort(key=sort, reverse=True)
    
    for user in top_users:
        pic = None
        try:
            pic = Profile.objects.get(user=user).profile_pic.url
        except:
            pic = static('unknown_profile.jpg')
        
        users.append({
            "id": user.pk,
            "name": f"{user.first_name} {user.last_name}",
            "pic": pic
        })

    data = {
        "category": category,
        "pub_count": published,
        "awaiting": awaiting,
        "users": users,
    }

    return render(request, 'home.html', data)
