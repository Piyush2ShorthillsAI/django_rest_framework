from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator



def alphanumberic(value):
    if not str(value).isalnum():
        raise ValidationError("Only aplhanumeric characters are allowed")
    return value
# Create your models here.


class Showroomlist(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    website = models.URLField(max_length=100)
    
    def __str__(self):
        return self.name
    # cars = models.ManyToManyField('carlist', related_name='showrooms', blank=True)

class carlist(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    chassisnumber = models.CharField(max_length=100, blank=True, null=True, validators=[alphanumberic])
    price  = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    showroom  = models.ForeignKey(Showroomlist, on_delete=models.CASCADE, related_name='cars', blank=True, null=True)
    def __str__(self):
        return self.name
    
class  Review(models.Model):
    rating   = models.IntegerField(validators=[MinValueValidator, MaxValueValidator])
    comments = models.CharField(max_length=200,null = True)
    car = models.ForeignKey(carlist, on_delete=models.CASCADE, related_name='reviews', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"the rating of {self.car.name} is :--- {self.rating}"