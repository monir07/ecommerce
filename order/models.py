from django.db import models 
from eshop.models import Product
from cart.models import Coupon
from django.contrib.auth import get_user_model
User = get_user_model()

class SizeOptions(models.TextChoices):
    """ CONSTANT = DB_VALUE, USER_DISPLAY_VALUE  """
    XS = 'xc', 'XC'
    S = 's', 'S'
    M = 'm', 'M'
    L = 'l', 'L'
    XL = 'xl', 'XL'

class ColorOptions(models.TextChoices):
    """ CONSTANT = DB_VALUE, USER_DISPLAY_VALUE  """
    BLACK = 'black', 'BLACK'
    WHITE = 'white', 'WHITE'
    RED = 'red', 'RED'
    BLUE = 'blue', 'BLUE'
    GREEN = 'green', 'GREEN'


# Create your models here.
class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name='ordered', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=10, choices=SizeOptions.choices)
    color = models.CharField(max_length=15, choices=ColorOptions.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = ('Received', 'On the way', 'Delivered')
    user = models.ForeignKey(User, related_name='orders', on_delete = models.CASCADE)
    order_items = models.ManyToManyField(OrderItem)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    address = models.TextField()
    total = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=True)
    transaction_id = models.UUIDField()
    status = models.CharField(max_length=15, choices=list(zip(STATUS_CHOICES, STATUS_CHOICES)))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.first_name + ' ' + self.last_name
