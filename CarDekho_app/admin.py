from django.contrib import admin
from .models import carlist, Showroomlist, Review
# Register your models here.
admin.site.register(carlist)
admin.site.register(Showroomlist)
admin.site.register(Review)