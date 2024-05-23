from django.db import models

class portfolio(models.Model):
    
    Name = models.CharField(max_length=256)
    Email = models.CharField(max_length=256)
    Message = models.CharField(max_length=256)
    
    def __str__(self):
        return self.Name