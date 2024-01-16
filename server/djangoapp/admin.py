from django.contrib import admin
# from .models import related models

from .models import *

# Register your models here.
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    fields = ['name','description']

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)
