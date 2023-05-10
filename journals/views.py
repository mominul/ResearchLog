from django.urls import reverse
from django.shortcuts import render,redirect
from journals.models import Publication, Category, Authorship
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import fitz
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.contrib import messages

# Create your views here.
def publications_view(request):
    # print(request.GET["title"], request.GET["category"])
    cate=[]
    for i in Category.objects.all():
        cate.append(i.category)

    pub=[]
    pub_list=[] 

    for i in Publication.objects.all():
        users=[]
        categories = []

        for c in i.category.all():
            categories.append(c.category)

        for j in i.authors.all():
            users.append({
                "name": f"{j.first_name} {j.last_name}",
                "id": j.id
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

@login_required
def upload_publication(request):
    if request.POST:
        print(request.POST)
        title = request.POST["title"]
        desc = request.POST["desc"]

        pub = Publication(title=title, description=desc)
        pub.save()
        
        pub.authors.add(request.user)

        # Co-authors
        if request.POST["authors"] != "":
            for author in request.POST["authors"].strip().split(','):
                try:
                    author = User.objects.get(username=author)
                    pub.authors.add(author)
                except:
                    messages.error(request, f"No registered user '{author}' found!")
                    pub.delete()
                    return redirect('/publications/upload')
        
        # Categories
        try:
            for category in request.POST["categories"]:
                category = Category.objects.get(id=category)
                pub.category.add(category)
        except:
            messages.error(request, "Please select a category!")
            pub.delete()
            return redirect('/publications/upload')

        # Pdf file processing
        try:
            pdf = request.FILES['pdf']
            pub.pdf = pdf
            
            pdf_doc = fitz.open(stream=pdf.read(), filetype='pdf')

            # Get the first page of the PDF
            first_page = pdf_doc.load_page(0)

            # Convert the first page to an image
            image_bytes = first_page.get_pixmap().tobytes()
            # Save the image data to the database
            pub.front_pic.save(f'{title}.png', ContentFile(image_bytes))
        except:
            messages.error(request, "Please select the PDF file of the paper!")
            pub.delete()
            return redirect('/publications/upload')
        
        pub.save()
        

    categories=[]
    for i in Category.objects.all():
        categories.append({ "id": i.pk, "category": i.category })
    
    data = {
        "categories": categories,
    }
    return render(request, 'upload.html', data)
def pdf_views(request):
    return render(request, 'pdfview.html')
