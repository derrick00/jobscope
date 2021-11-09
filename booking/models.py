from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from service.models import Service

# Create your models here.
class Booking(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    telephone=models.CharField(max_length=12, blank=False)
    email=models.EmailField(max_length=200)
    location=models.CharField(max_length=200)
    paid=models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'booking'
        verbose_name_plural = 'bookings'
    
    def __str__(self):
        return 'Booking {}'.format(self.id)
    def get_absolute_url(self):
        return reverse('jobscope:category_services', args=[self.slug])



