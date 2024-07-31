from django.test import TestCase
from django.contrib.auth.models import User
from .models import MenuItem, OrderItem, Order
from decimal import Decimal

class MenuItemModelTest(TestCase):

    def setUp(self):
        # creating new test user and menuitem
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.menu_item = MenuItem.objects.create(
            creator=self.user,
            category='MC',
            name='Test dish',
            description='A  test dish',
            price=Decimal('1000.00'),
            percentage_discount=10,
            available=True,
            tags='test, dish',
            order=1
        )

    def test_menu_item_creation(self):
        # testing the menu fields are correctly set
        self.assertEqual(self.menu_item.name, 'Test dish')
        self.assertEqual(self.menu_item.get_price(), Decimal('900.00'))  # 10% discount on 1000
        self.assertTrue(self.menu_item.available)
        self.assertEqual(self.menu_item.tags, 'test, dish')

    def test_menu_item_string_representation(self):
        self.assertEqual(str(self.menu_item), 'Test dish')


class OrderItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.menu_item = MenuItem.objects.create(
            creator=self.user,
            name='Test dish',
            price=Decimal('1000.00')
        )
        self.order_item = OrderItem.objects.create(
            menu_item=self.menu_item,
            quantity=2
        )
    def test_order_item_creation(self):
        #test correctness of set fields again

        self.assertEqual(self.order_item.menu_item, self.menu_item)
        self.assertEqual(self.order_item.quantity, 2)


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.menu_item = MenuItem.objects.create(
            creator=self.user,
            name='Test dish',
            price=Decimal('1000.00')
        )
        self.order_item = OrderItem.objects.create(
            menu_item=self.menu_item,
            quantity=2
        )
        self.order = Order.objects.create(
            customer=self.user,
            status='PL',
            payment_method='ON',
            shipping_address='123 Test St'
        )
        self.order.items.add(self.order_item)

    def test_order_creation(self):
        
    #test correctness of set fields again
        self.assertEqual(self.order.customer, self.user)
        self.assertEqual(self.order.status, 'PL')
        self.assertEqual(self.order.payment_method, 'ON')
        self.assertEqual(self.order.shipping_address, '123 Test St')

    def test_order_total(self):
        
        self.assertEqual(self.order.get_total(), Decimal('2000.00'))  # 2 items * 1000.00 each
