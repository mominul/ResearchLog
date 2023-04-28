from django.shortcuts import render,redirect
from journals.models import Publication, Category, Authorship
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import fitz
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

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

@login_required
@csrf_exempt
def upload_journal(request):
    if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            pdf = request.FILES['pdf']
            pdf_doc = fitz.open(stream=pdf.read(), filetype='pdf')

            # Get the first page of the PDF
            first_page = pdf_doc.load_page(0)

            # Convert the first page to an image
            image_bytes = first_page.get_pixmap().tobytes()

            # Save the image data to the database
            new_joural=Publication(title=title,description=description,pdf=pdf)
            new_joural.frond_pic.save(f'{title}.png', ContentFile(image_bytes))
            new_joural.save()
        
    return redirect('/uplode-journal')




