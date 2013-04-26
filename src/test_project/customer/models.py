from django.db import models
from django import forms
from django.contrib import admin

# Create your models here.
class Customer(models.Model):
        Name = models.CharField(max_length=50)

