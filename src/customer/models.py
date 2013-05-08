from django.db import models


class Customer(models.Model):
        name = models.CharField(max_length=50)
        address = models.ForeignKey('Address')

class Address(models.Model):
    zip_code = models.IntegerField()
    street = models.CharField(max_length=64)
