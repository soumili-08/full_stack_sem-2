from django.urls import path
from .views import admin_page

urlpatterns = [
    path('admin/', admin_page, name='admin_page'),
]