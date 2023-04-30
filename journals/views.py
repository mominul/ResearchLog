from django.shortcuts import render
from journals.models import Publication, Category, Authorship
from django.contrib.auth.models import User

# Create your views here.
def publications_view(request):
    # print(request.GET["title"], request.GET["category"])
    cate=[]
    for i in Category.objects.all():
        cate.append(i.category)

    pub=[]
    pub_list=[] 

    for i in Publication.objects.all():
        authors = Authorship.objects.filter(publication=i)
        users=[]
        categories = []

        for c in i.category.all():
            categories.append(c.category)

        for j in authors.all():
            users.append({
                "name": f"{j.user.first_name} {j.user.last_name}",
                "id": j.user.id
            })
        
        dict = {
            "authors":users,
            "title":i.title,
            "desc": i.description,
            "categories": categories,
        }
        pub_list.append(dict)

    filtered_publications = []

    if request.GET.get("category"):
        for pub in pub_list:
            if request.GET["category"] in pub["categories"]:
                filtered_publications.append(pub)
    else:
        filtered_publications = pub_list

    data = {
        "category":cate,
        "publications":filtered_publications,
    }
    return render(request, "list.html",data)