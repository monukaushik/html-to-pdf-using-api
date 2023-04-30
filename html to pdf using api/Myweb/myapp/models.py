from django.db import models

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=30)
    subject=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    image=models.ImageField(upload_to ='uploads/')

    
    def __str__(self):
        return self.name