from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.ListOfOrdersView.as_view(), name='list-orders'),
    path('new-order/', views.CreateOrderView.as_view(), name='new-order'),
    path('orders/<int:pk>/', views.DetailOrdersView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update/', views.UpdateOrdersView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', views.DeleteOrdersView.as_view(), name='order_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('goods/', views.ListOfItemsView.as_view(), name='list-goods'),
    path('new-goods/', views.CreateItemView.as_view(), name='new-goods'),
    path('goods/<int:pk>/', views.DetailItemView.as_view(), name='item_detail'),
    path('goods/<int:pk>/update/', views.UpdateItemView.as_view(), name='item_update'),
    path('goods/<int:pk>/delete/', views.DeleteItemView.as_view(), name='item_delete'),
]
