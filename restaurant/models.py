from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from decimal import Decimal

PAYMENT_METHODS = (("CS", "Cash"), ("ON", "Online"))

APPETIZER = 'AP'
MAIN_COURSE = 'MC'
DESSERT = 'DS'
BEVERAGE = 'BV'

# Food Menu Category Key,Value Tuple 
CATEGORY_CHOICES = [
        (APPETIZER, 'Appetizer'),
        (MAIN_COURSE, 'Main Course'),
        (DESSERT, 'Dessert'),
        (BEVERAGE, 'Beverage/Drink'),
    ]

# Food Menu Model 
class MenuItem(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=MAIN_COURSE,
    )    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    percentage_discount = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    accepted_payment_methods = MultiSelectField(default=['ON', 'CS'], choices=PAYMENT_METHODS ) #Payment method allowed for this item 
    tags = models.CharField(max_length=100, blank=True, help_text='Comma Separated Values')  # comma-separated tags
    order = models.PositiveIntegerField(default=0) #for sorting items , higher number/value appears among the top
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def get_price(self):
        if self.percentage_discount:
            discount = Decimal(self.percentage_discount / 100) * self.price 
            price = self.price - discount
            return price.__round__()
        else:
            return self.price 
    def __str__(self):
        return self.name
    
#Customer OrderItem Model
class OrderItem (models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
# Customer Main Order Model 
RECEIVED= 'RC' #When Order has been received by the customer 
PLACED =  'PL' #When Order has been created and customer has made payment 
DELIVERED = 'DL' #When Order has been delivered to the customer
CANCELLED = 'CA' #When Order is cancelled by staff or customer due to failed delivery or other possible circumstances

ORDER_STATUS_CHOICES = (
    (PLACED,'Placed'),
    (DELIVERED,'Completed'),
    (DELIVERED,'Delivered'),
    (CANCELLED,'Cancelled'),
)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, related_name='root_order')
    status = models.CharField(max_length=20, default=PLACED, choices=ORDER_STATUS_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    shipping_address = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def get_total(self):
        # get each item, multiply by quantity and sum all to return order total 
        total_on_items = sum([item.quantity * item.menu_item.get_price()  for item in self.items.all() ])
        return total_on_items