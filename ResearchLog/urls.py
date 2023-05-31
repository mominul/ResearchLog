"""ResearchLog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import home_view
import profile.views as profile_view
from journals.views import publications_view
from django.conf import settings
from django.conf.urls.static import static
from journals.views import upload_publication, view_publication, approve_publications, approve_publication, delete_publication, update_publication

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('login/', profile_view.login_page, name='login'),
    path('logout/',profile_view.logout_page, name='logout'),
    path('signup/',profile_view.signup_view, name='signup'),
    path('activate/<uid>/<token>', profile_view.activate, name="activate"),
    path('forgot-password', profile_view.forgot_password,name='forgot_password'),
    path('forgot-password/<uid>/<token>', profile_view.forgot_password_active_url,name='forgot_password_url'),
    path('reset-password', profile_view.reset_password,name='reset_password'),
    path('profile/<int:id>',profile_view.profile_view, name='profile_view'),
    path('profile_update/',profile_view.profile_update_view, name='profile_update'),
    path('publications/',publications_view, name='publications'),
    path('publications/upload',upload_publication, name='upload_pub'),
    path('publications/view/<int:id>', view_publication, name='publication_view'),
    path('publications/approve/', approve_publications, name='publications_approve'),
    path('publications/approve/<int:id>', approve_publication, name='approve_publication'),
    path('publications/delete/<int:id>', delete_publication, name='delete_publication'),
    path('publications_update/', update_publication, name='update_publication'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
