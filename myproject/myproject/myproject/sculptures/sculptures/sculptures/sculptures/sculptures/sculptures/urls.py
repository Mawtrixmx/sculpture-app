from django.urls import path
from . import views

app_name = 'sculptures'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('upload/', views.upload_sculpture, name='upload'),
    path('gallery/', views.gallery, name='gallery'),
]
