from django.shortcuts import render
from journals.models import Publication, Category, Authorship
from django.contrib.auth.models import User

# Create your views here.
def category(request):
    cate=[]
    for i in Category.objects.all():
        cate.append(i.category)

    pub=[]
    pub_list=[] 

    for i in Publication.objects.all():
        # pub.append(i.title)
        authors = Authorship.objects.filter(publication=i)
        users=[]

        for j in authors.all():
            users.append(j.user.first_name)
        pub_lst = {
                "users":users,
                "title":j.publication.title
            }
        pub.append(pub_lst)

    data = {
        "category":cate,
        "title":pub
    }
    return render(request, "list.html",data)