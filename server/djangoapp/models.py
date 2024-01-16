from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null= False, max_length=30, default='Audi')
    description = models.CharField(null= False, max_length=300, default='Audi cars are aight')

    def __str__(self):
        return 'Name:' + self.name + ',' + \
            'Description:' + self.description


class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    OTHERS = 'others'
    CAR_CHOICES = [(SEDAN, "Sedan"), (SUV, 'SUV'), (WAGON, 'Wagon'), (OTHERS, 'Others')]
    carmake = models.ForeignKey(CarMake, null= True, on_delete=models.CASCADE)
    name = models.CharField(null= False, max_length=30, default='Audi X8')
    dealerid = models.IntegerField(null=True)
    cartype = models.CharField(null= False, max_length=20, choices= CAR_CHOICES, default=SEDAN)
    year = models.DateField(null= True)

    def __str__(self):
        return 'Name ' + self.name

