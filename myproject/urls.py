"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from . import views

from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    # path('upload-member-file/', views.upload_member_file, name='upload_member_file'),
    # path('upload-palms-report/', views.upload_palms_report, name='upload_palms_report'),
    path('upload-both-reports/', views.upload_both_reports, name='upload_both_reports'),
    path('final-data/', views.final_data_view, name='final_data'),  # Add this line
    path('export-go-green-excel/', views.export_go_green_excel, name='export_go_green_excel'),
]
