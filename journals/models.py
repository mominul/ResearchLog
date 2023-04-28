from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category=models.CharField(max_length=250)

class Publication(models.Model):
    title=models.TextField()
    description=models.TextField(null=True)
    frond_pic=models.ImageField(upload_to='publications/',null=True, blank=True)
    pdf=models.FileField(upload_to='publications/',null=True, blank=True)
    is_approved= models.BooleanField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    

class Authorship(models.Model):
    publication=models.ForeignKey(Publication,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
