from django.db import models
from category.models import Category

class Product(models.Model):
    name = models.CharField(max_length=100)	
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name