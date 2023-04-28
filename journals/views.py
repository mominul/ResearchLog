from django.shortcuts import render
from journals.models import Publication, Category, Authorship
from django.contrib.auth.models import User

# Create your views here.
def publications_view(request):
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
            users.append({
                "name": f"{j.user.first_name} {j.user.last_name}",
                "id": j.user.id
            })
        
        pub_lst = {
            "authors":users,
            "title":i.title,
            "desc": i.description,
        }
        pub.append(pub_lst)

    data = {
        "category":cate,
        "publications":pub
    }
    return render(request, "list.html",data)