from django.urls import reverse
from django.shortcuts import render,redirect
from journals.models import Publication, Category, Authorship
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import fitz
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

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

    if request.GET.get("category") and request.GET.get("category") != "none":
        for pub in pub_list:
            if request.GET["category"] in pub["categories"]:
                filtered_publications.append(pub)
    else:
        filtered_publications = pub_list

    if request.GET.get("title"):
        filtered = []
        search = request.GET["title"].casefold()
        for pub in filtered_publications:
            if search in pub["title"].casefold():
                filtered.append(pub)
        filtered_publications = filtered

    data = {
        "category":cate,
        "publications":filtered_publications,
    }
    return render(request, "list.html",data)

@login_required
@csrf_exempt
def upload_journal(request):
    if request.method == 'POST':
            title = request.POST['title']
            # description = request.POST['description']
            pdf = request.FILES['pdf']
            pdf_doc = fitz.open(stream=pdf.read(), filetype='pdf')

            # Get the first page of the PDF
            first_page = pdf_doc.load_page(0)

            # Convert the first page to an image
            image_bytes = first_page.get_pixmap().tobytes()
            # Save the image data to the database
            new_joural=Publication(title=title,pdf=pdf)
            new_joural.front_pic.save(f'{title}.png', ContentFile(image_bytes))
            new_joural.save()
            new_author=Authorship(publication=new_joural)
            new_author.user=request.user            
            new_author.save()

        
    return redirect(reverse('profile_update'))

def upload_publication(request):
    return render(request, 'upload.html')
def pdf_views(request):
    return render(request, 'pdfview.html')
