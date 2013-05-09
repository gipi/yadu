from django.db import models


class Customer(models.Model):
        name = models.CharField(max_length=50)
        address = models.ForeignKey('Address')

class ZipCode(models.Model):
    state = models.CharField(max_length=100)

class Address(models.Model):
    zip_code = models.ForeignKey(ZipCode)
    street = models.CharField(max_length=64)
