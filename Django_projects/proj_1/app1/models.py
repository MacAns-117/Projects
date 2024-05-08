from django.db import models

# Create your models here.
class Patient(models.Model):
    Name = models.CharField(max_length=256)
    Blood_group=models.CharField(max_length=100)
    Age=models.IntegerField()
    Disease = models.CharField(max_length=256)
    Location = models.CharField(max_length=256)
    def __str__(self):
        return self.Name