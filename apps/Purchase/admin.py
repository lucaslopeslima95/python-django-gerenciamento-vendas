from django.contrib import admin
from .models import Purchase
from .models import PurchaseItem
from .models import DeadLine
from .models import info_utils


admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(DeadLine)
admin.site.register(info_utils)
