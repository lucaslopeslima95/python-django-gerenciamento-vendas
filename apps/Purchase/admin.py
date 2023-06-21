from django.contrib import admin
from .models import Purchase
from .models import PurchaseItem

admin.site.register(Purchase)
admin.site.register(PurchaseItem)