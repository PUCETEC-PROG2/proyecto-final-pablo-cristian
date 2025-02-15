from django.urls import path
from . import views

urlpatterns = [
    # Núcleo
    path('', views.welcome, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('welcome/', views.welcome, name='welcome'),


    # Productos
    path('products/', views.products, name='products'),


    # Clientes

    path('clientes/', views.clients, name='clientes'),  
    path('clientes/add/', views.add_client, name='add_client'),
    path('clientes/edit/<int:client_id>/', views.edit_client, name='edit_client'),
    path('clientes/delete/<int:client_id>/', views.delete_client, name='delete_client'),

    # Compras
    path('compras/', views.purchases, name='compras'),
    path('compras/nueva/', views.add_purchase, name='nueva_compra'),
    path('compras/<int:pk>/', views.purchase_details, name='detalle_compra'),
]
