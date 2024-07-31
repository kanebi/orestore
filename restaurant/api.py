from rest_framework.viewsets import ModelViewSet, ViewSet, ReadOnlyModelViewSet,GenericViewSet
from rest_framework.views import APIView, Response, status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404 

from rest_framework.serializers import ValidationError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import MenuItemSerializer,OrderItemSerializer, OrderSerializer, CreateOrderSerializer,UpdateStatusOrderSerializer,OrderItemCreationSerializer
from .models import MenuItem, Order, OrderItem,BEVERAGE,PLACED,RECEIVED,CANCELLED
import json

# customer is same as user in any block and both words can be used interchangeably 

    
# Api for all menu items 
class MenuItems(ReadOnlyModelViewSet):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all().order_by('-order')
    
# Api for menu items that has discount 
class DiscountedMenuItems(ReadOnlyModelViewSet):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all().order_by('-order')
    def get_queryset(self):
        qs= super().get_queryset()
        # filter the queryset/items from the db model to return only menu items with percentage discount greater than or equal to 1
        filtered_qs = qs.filter(percentage_discount__gte=1)
        return filtered_qs

    
# Api for menu items that are of drink/beverage category 
class   BeverageMenuItems(ReadOnlyModelViewSet):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all().order_by('-order')
    
    def get_queryset(self):
        qs= super().get_queryset()
        # filter the queryset from the db model to return only beverages
        filtered_qs = qs.filter(category =  BEVERAGE)
        return filtered_qs
    
    
    
# Api for authenticated user order. can only be viewed by authenticated user 
class  UserOrders(ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes =[IsAuthenticated]
    
    def get_queryset(self):
        qs= super().get_queryset()
        # filter the queryset from the db model to return only orders created by user/customer 
        filtered_qs = qs.filter(customer=self.request.user)
        return filtered_qs
    
    
    
class CreateOrder(GenericViewSet):
    permission_classes = [IsAuthenticated] #only authenticated user can perform the actions order 
    serializer_class = CreateOrderSerializer
    def post(self, request):
        # parse request data if it is string else return json data as it is 
        request_data :dict["payment_method":str, 'shipping_address':str, 'items':list]= self.request.data if not   isinstance(self.request.data, str)  else json.loads(self.request.data) 
        # get the menu items and quantity from the request 
        menu_items :list = request_data.get('items')
        order_detail  = request_data
        if order_detail:
            order_detail.setdefault('customer',self.request.user.id)
            order = self.serializer_class(data =order_detail)
            # validate user order and create using order class  serializer 
            if order.is_valid():
                order =order.save()
                order.status = PLACED
                order.save()
            return   Response ( OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return   Response ({'error':"Please provide order info"}, status=status.HTTP_403_FORBIDDEN)

class UpdateOrderStatus(GenericViewSet):
    permission_classes = [IsAuthenticated] #only authenticated user can perform the actions order 
    serializer_class = UpdateStatusOrderSerializer
    def put(self):
        # define what action users can perform on update of order 
        allowed_customer_update_action = [RECEIVED, CANCELLED]
        request_data = self.request.data
        update_action = request_data.get('update_action')
        # permission check 
        if not update_action in allowed_customer_update_action:
            
            return Response({'error':'You cannot perform this update'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            order = get_object_or_404(Order, id=request_data.get('order_id'))
            order.status = update_action
            order.save()
            return   Response (OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    
            
    