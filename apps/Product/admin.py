from django.contrib import admin
from .models import Product
from .models import StoreStock
from .models import Warehouse


admin.site.register(Product)
admin.site.register(StoreStock)
admin.site.register(Warehouse)
