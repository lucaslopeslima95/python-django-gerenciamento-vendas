from Category import urls as category_urls
from Collaborator import urls as collaborator_urls
from Dashboard import urls as dashboard_urls
from django.contrib import admin
from django.urls import include, path
from Product import urls as product_urls
from Purchase import urls as purchase_urls
from Reports import urls as reports_urls
from Stock import urls as stock_urls
from User import urls as User_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(User_urls, namespace='user'), name="user"),
    path("colaborador/", include(collaborator_urls,
                                 namespace="collaborator"),
         name="collaborator"),
    path("produtos/", include(product_urls,
                              namespace="product"), name="product"),
    path("compras/", include(purchase_urls,
                             namespace="purchase"), name="purchase"),
    path("categorias/", include(category_urls,
                                namespace="category"), name="category"),
    path("estoque/", include(stock_urls, namespace="stock"), name="stock"),
    path("relatorios/", include(reports_urls, namespace="reports"),
         name="reports"),
    path("painel/", include(dashboard_urls, namespace="dashboard"),
         name="dashboard"),
]
