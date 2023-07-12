from django.contrib import admin
from .models import Product
from .models import StoreStock
from .models import Warehouse
from .models import LogWarehouse
from .models import LogStoreStock


admin.site.register(Product)
admin.site.register(StoreStock)
admin.site.register(Warehouse)
admin.site.register(LogStoreStock)
admin.site.register(LogWarehouse)
