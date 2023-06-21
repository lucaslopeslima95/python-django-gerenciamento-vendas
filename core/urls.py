from django.contrib import admin
from django.urls import path,include
from User import urls as User_urls
from Collaborator import urls as collaborator_urls
from Product import urls as product_urls
from Purchase import urls as purchase_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(User_urls,namespace='user'),name="home"),
    path("collaborator/",include(collaborator_urls,namespace="collaborator"),name="collaborator"),
    path("product/",include(product_urls,namespace="product"),name="product"),
    path("purchase/",include(purchase_urls,namespace="purchase"),name="purchase"),
]
