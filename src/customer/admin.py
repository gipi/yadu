from django.contrib import admin
from yadu.admin import RelatedFieldAdmin

from .models import Customer

class CustomerAdmin(RelatedFieldAdmin):
    list_display = [
        'name',
        'address__street'
    ]

admin.site.register(Customer, CustomerAdmin)
