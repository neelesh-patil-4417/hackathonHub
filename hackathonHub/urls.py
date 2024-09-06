"""
URL configuration for hackathonHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from hackmanage.views import hackathon_list,hackathon_create,register_hackathon,enrolled_hackathons,list_submissions,create_submission,signup,login
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('hackathons/',hackathon_list),
    path('createhackathons/',hackathon_create),
    path('register/',register_hackathon),
    path('hackathons-enrolled/',enrolled_hackathons),
    path('listsubmissions/',list_submissions),
    path('createsubmission/',create_submission),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
