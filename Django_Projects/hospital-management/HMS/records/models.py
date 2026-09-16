from django.db import models


class Patient(models.Model):
    BLOOD_GROUPS = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    name = models.CharField(max_length=256)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)
    age = models.PositiveIntegerField()
    disease = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Nurse(models.Model):
    GENDER_CHOICES = [("F", "Female"), ("M", "Male")]
    SHIFT_CHOICES = [
        ("5:00 AM - 1:00 PM", "5:00 AM - 1:00 PM"),
        ("1:00 PM - 9:00 PM", "1:00 PM - 9:00 PM"),
        ("9:00 PM - 5:00 AM", "9:00 PM - 5:00 AM"),
    ]
    DEPARTMENT_CHOICES = [
        ("Cardiology", "Cardiology"),
        ("Gynecology", "Gynecology"),
        ("Orthopedics", "Orthopedics"),
        ("General", "General"),
    ]

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    shift = models.CharField(max_length=50, choices=SHIFT_CHOICES)
    care = models.CharField(max_length=100, help_text="Type of care")
    experience = models.PositiveIntegerField(help_text="Years")
    certifications = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="nurse_pics/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
