from django.urls import reverse
from django.shortcuts import render,redirect
from journals.models import Publication, Category
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

    for i in Publication.objects.filter(is_approved=True):
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
            "id": i.pk,
            "authors":users,
            "title":i.title,
            "desc": i.description,
            "categories": categories,
            "image": i.front_pic.url,
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
def upload_publication(request):
    if request.POST:
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
        messages.success(request, "Paper added to the approval queue succesfully!")
        return redirect('/')

    categories=[]
    for i in Category.objects.all():
        categories.append({ "id": i.pk, "category": i.category })
    
    data = {
        "categories": categories,
    }
    return render(request, 'upload.html', data)

@login_required
def update_publication(request, id):
    pub = Publication.objects.get(id=id)
    if request.POST:
        print(request.POST)
        title = request.POST["title"]
        pub.title = request.POST["title"]
        pub.description = request.POST["desc"]

        # Co-authors
        if request.POST["authors"] != "":
            authors = str(request.POST["authors"])
            if authors.endswith(','):
                authors = authors[:-1]
            pub.authors.clear()
            for author in authors.strip().split(','):
                try:
                    author = User.objects.get(username=author)
                    pub.authors.add(author)
                except:
                    print(list(request.POST["categories"]))
                    messages.error(request, f"No registered user '{author}' found!")
                    return redirect(f'/publications/update/{id}')

        # Categories
        try:
            for category in request.POST["categories"]:
                # print(category)
                category = Category.objects.get(id=category)
                pub.category.add(category)
        except:
            messages.error(request, "Please select a category!")
            return redirect(f'/publications/update/{id}')

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
            pass
        
        pub.save()
        messages.success(request, "Paper updated succesfully!")
        return redirect(f'/publications/view/{id}')

    categories =[]
    for cat in Category.objects.all():
        categories.append({
            "id": cat.id,
            "category": cat.category,
            "selected": cat in pub.category.all(),
        })
    
    authors = ""

    for author in pub.authors.all():
        authors += f"{author.username},"

    data = {
        "title": pub.title,
        "desc": pub.description,
        "authors": authors,
        "categories": categories,
        "file": pub.pdf.url,
    }
    return render(request, 'paper_update.html', data)

def view_publication(request, id):
    pub = Publication.objects.get(id=id)

    authors = []
    for author in pub.authors.all():
        authors.append({
            "id": author.pk,
            "name": f"{author.first_name} {author.last_name}",
        })
    
    categories = []
    for category in pub.category.all():
        categories.append(category.category)

    show_button = request.user in pub.authors.all()
    
    data = {
        "id": id,
        "title": pub.title,
        "desc": pub.description,
        "authors": authors,
        "categories": categories,
        "pdf": pub.pdf.url,
        "image": pub.front_pic.url,
        "show_button": show_button,
    }
    return render(request, 'pdfview.html', data)

@login_required
def update_publication(request):
    # data = {}
    # if request.user.is_authenticated:      
    #     if request.method == 'POST':
    #         title = request.POST["title"]
    #         desc = request.POST["desc"]
    #         category = request.POST['category']
    #         authors = request.POST['authors']
    #         publication = None
            

    #         if Publication.authors.user.objects.filter(user_id= request.user.id):
    #             publication = Publication.authors.user.objects.get(user_id= request.user.id)
    #         else:
    #             publication = Publication.authors.user(user_id = request.user.id)

    #         # Profile pic
    #         try:
    #             front_pic = request.FILES['front_pic']
    #             publication.front_pic = front_pic
    #         except:
    #             pass
            
    #         user = request.user
    #         publication.title = title
    #         publication.description = desc
    #         publication.save()
    #         print("Saved!")
    #         return redirect(f'/pdfview/{user.id}')
    #     else:
    #         publication = None
    #         publication = Publication(title=title, description=desc)
    #         print(user)

    #         data = {
    #             'title': publication.title,
    #             'desc': publication.desc,
    #         }
    # return render(request, 'update_journal.html',data)
    return render(request, 'update_journal.html')

@login_required
def approve_publications(request):
    if request.user.is_staff:
        list = []
        for pub in Publication.objects.filter(is_approved=False):
            list.append({
                'id': pub.pk,
                'title': pub.title,
                'image': pub.front_pic.url,
            })
        
        data = {
            'publications': list,
        }
        return render(request, 'approve.html', data)
    
    return redirect('/')

@login_required
def approve_publication(request, id):
    if request.user.is_staff:
        pub = Publication.objects.get(id=id)
        pub.is_approved = True
        pub.save()
        return redirect('/publications/approve/')
    
    return redirect('/')

@login_required
def delete_publication(request, id):
    if request.user.is_staff:
        pub = Publication.objects.get(id=id)
        pub.delete()
        return redirect('/publications/approve/')
    
    return redirect('/')
