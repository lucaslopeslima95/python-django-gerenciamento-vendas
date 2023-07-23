from django.contrib import admin
from .models import Purchase
from .models import PurchaseItem
from .models import DeadLine

admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(DeadLine)
