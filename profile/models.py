from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/', null=True, blank=True)
    description = models.TextField(null=True)
    scholar_id = models.CharField(max_length=255, null=True)
    gh_id = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.user.first_name
