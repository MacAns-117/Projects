from django.db import models

class Task(models.Model):
    task_name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.task_name
