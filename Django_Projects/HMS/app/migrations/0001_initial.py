# Generated by Django 5.0.4 on 2024-06-12 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=1)),
                ('department', models.CharField(max_length=100)),
                ('shift', models.CharField(choices=[('5:00 AM - 1:00 PM', '5:00 AM - 1:00 PM'), ('1:00 PM - 9:00 PM', '1:00 PM - 9:00 PM'), ('9:00 PM - 5:00 AM', '9:00 PM - 5:00 AM')], max_length=20)),
                ('care', models.CharField(max_length=100)),
                ('experience', models.PositiveIntegerField()),
                ('certifications', models.CharField(blank=True, max_length=255)),
                ('contact_number', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('profile_picture', models.ImageField(blank=True, upload_to='nurses/')),
            ],
        ),
    ]