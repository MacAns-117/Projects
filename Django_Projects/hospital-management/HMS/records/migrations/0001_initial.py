from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=256)),
                (
                    "blood_group",
                    models.CharField(
                        choices=[
                            ("A+", "A+"),
                            ("A-", "A-"),
                            ("B+", "B+"),
                            ("B-", "B-"),
                            ("AB+", "AB+"),
                            ("AB-", "AB-"),
                            ("O+", "O+"),
                            ("O-", "O-"),
                        ],
                        max_length=5,
                    ),
                ),
                ("age", models.PositiveIntegerField()),
                ("disease", models.CharField(max_length=256)),
                ("location", models.CharField(max_length=256)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Nurse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("gender", models.CharField(choices=[("F", "Female"), ("M", "Male")], max_length=1)),
                (
                    "department",
                    models.CharField(
                        choices=[
                            ("Cardiology", "Cardiology"),
                            ("Gynecology", "Gynecology"),
                            ("Orthopedics", "Orthopedics"),
                            ("General", "General"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "shift",
                    models.CharField(
                        choices=[
                            ("5:00 AM - 1:00 PM", "5:00 AM - 1:00 PM"),
                            ("1:00 PM - 9:00 PM", "1:00 PM - 9:00 PM"),
                            ("9:00 PM - 5:00 AM", "9:00 PM - 5:00 AM"),
                        ],
                        max_length=50,
                    ),
                ),
                ("care", models.CharField(help_text="Type of care", max_length=100)),
                ("experience", models.PositiveIntegerField(help_text="Years")),
                ("certifications", models.CharField(blank=True, max_length=255)),
                ("contact_number", models.CharField(max_length=15)),
                ("email", models.EmailField(max_length=254)),
                ("address", models.TextField(blank=True)),
                ("profile_picture", models.ImageField(blank=True, null=True, upload_to="nurse_pics/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
    ]
