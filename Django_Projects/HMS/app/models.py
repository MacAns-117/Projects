from django.db import models

class Nurse(models.Model):
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
    ]

    SHIFT_CHOICES = [
        ('5:00 AM - 1:00 PM', '5:00 AM - 1:00 PM'),
        ('1:00 PM - 9:00 PM', '1:00 PM - 9:00 PM'),
        ('9:00 PM - 5:00 AM', '9:00 PM - 5:00 AM'),
    ]

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    department = models.CharField(max_length=100)
    shift = models.CharField(max_length=50)
    care = models.CharField(max_length=100)
    experience = models.IntegerField()
    certifications = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='nurse_pics/', blank=True, null=True)

    def __str__(self):
        return self.name
