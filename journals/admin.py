from django.contrib import admin
from journals.models import Publication, Category

class PublicationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Publication, PublicationAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)
