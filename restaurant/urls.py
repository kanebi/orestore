from django.urls import path, include
from rest_framework import routers
from .api import MenuItems, DiscountedMenuItems, BeverageMenuItems, UserOrders, CreateOrder, UpdateOrderStatus
from .views import menuitem_view

router = routers.DefaultRouter()
router.register(r'menus/discounted', DiscountedMenuItems,
                basename='discounted-menus')
router.register(r'menus/drinks', BeverageMenuItems, basename='drink-menus')
router.register(r'menus', MenuItems, basename='all-menus')
router.register(r'orders', UserOrders, basename='user-orders')

urlpatterns = [

    path(r'create-order', CreateOrder.as_view({'post':'post'}), name='create-order'),
    path('', include(router.urls)),

    path(r'update-order',  UpdateOrderStatus.as_view({'put':'put'}), name='update-order'),

]
