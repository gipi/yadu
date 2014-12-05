from django.contrib import admin
from yadu.admin_utils import RelatedFieldAdmin

from .models import Customer

class CustomerAdmin(RelatedFieldAdmin):
    list_display = [
        'name',
        'address__street',
        'address__zip_code__state',
    ]
    list_filter = [
        'address__street',
    ]

admin.site.register(Customer, CustomerAdmin)
