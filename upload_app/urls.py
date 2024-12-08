from django.urls import path
from .import views 
app_name = 'upload_app'

urlpatterns = [
    path('upload/', views.upload_app, name="upload_app"),
    
]