from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User 

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('jobscope:category_services', args=[self.slug])


class Service(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True) 
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

   # class Meta:
       # ordering = ('name',)
       # index_together = (('id', 'slug'),)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('jobscope:service_detail', args=[self.id, self.slug])
class Feedback(models.Model):
    name =models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
