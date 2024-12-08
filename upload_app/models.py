from django.db import models

# Create your models here.
class UploadedImage(models.Model):
    """Model for images"""
    title = models.CharField(max_length=100) # Title for images
    image = models.ImageField(upload_to='uploaded_images/') #Save images to this folder

    def __str__(self):
        return self.title