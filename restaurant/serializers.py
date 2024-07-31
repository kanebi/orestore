from rest_framework import serializers 

from .models import MenuItem, Order, OrderItem,ORDER_STATUS_CHOICES,User



# Serializer for MenuItem Model
class MenuItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    actual_price = serializers.SerializerMethodField()
    class Meta:
        model = MenuItem
        fields = '__all__'
    def get_actual_price(self, obj):
        return obj.price
    def get_price(self, obj):
        return obj.get_price()

    def get_category(self, obj):
        return obj.get_category_display()

# Serializer for OrderItem Model
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer()
    class Meta:
        model = OrderItem
        fields = '__all__'
        
# Serializer for Order Model
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    payment_method = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = '__all__'
    
    def get_total(self, obj):  
        return obj.get_total()
    def get_status(self, obj):  
        return obj.get_status_display()
    def get_payment_method(self, obj):  
        return obj.get_payment_method_display()
        
# Serializer for creating new order item
class OrderItemCreationSerializer (serializers.Serializer):
    item = serializers.CharField()
    quantity = serializers.IntegerField()
    def create(self,validated_data):
        instance = OrderItem.objects.create( menu_item= MenuItem.objects.get(id=validated_data.get('item')),quantity=validated_data.get('quantity'))
        return instance
    
# Serializer for creating new order
class CreateOrderSerializer (serializers.Serializer):
    shipping_address = serializers.CharField()
    payment_method = serializers.CharField()
    items = OrderItemCreationSerializer(many=True)
    customer = serializers.CharField()
    def to_internal_value(self, data):
        
        # change ids to model items 
        data['customer'] = User.objects.get(id = data['customer'])
        items = data['items'] 
        saved_items =set()
        # save all menu items and append them to the saved array so we can add them to the order object 
        for item in items:
            # create each item 
            model_item = OrderItemCreationSerializer(data =item)
            if model_item.is_valid():
                saved_item =model_item.save()
                saved_items.add(saved_item)
        data['items'] = saved_items
        return data
    
    def create(self, validated_data):
        items = validated_data.pop('items', [])
        instance = Order.objects.create(**validated_data)
        instance.save()
        instance.items.set(items)
        return instance
        
    
    
    
# Serializer for updating existing order status
class UpdateStatusOrderSerializer (serializers.Serializer):
    update_action = serializers.CharField()
    order_id = serializers.IntegerField()
    
    