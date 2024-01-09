from django.db import models

# Create your models here.

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    ratting = models.CharField(max_length=10)
    image = models.URLField()
    price = models.CharField(max_length=50)
    instock = models.BooleanField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title