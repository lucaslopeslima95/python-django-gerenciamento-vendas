from django.contrib import admin
from .models import StoreStock
from .models import Warehouse
from .models import LogWarehouse
from .models import LogStoreStock


admin.site.register(StoreStock)
admin.site.register(Warehouse)
admin.site.register(LogStoreStock)
admin.site.register(LogWarehouse)
