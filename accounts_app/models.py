from django.db import models

# Create your models here.
class Harvests_list(models.Model):
    """harvests_list table"""
    # Add the user field
    name = models.CharField(max_length = 100)
    produce_name = models.EmailField()
    quantity = models.CharField(max_length=255)
    location = models.TextField()
    
    def __str__(self):
        return self.name
    
