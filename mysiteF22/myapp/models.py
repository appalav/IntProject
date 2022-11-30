from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=20, null=True)

    def __str__(self):
        return 'Category {}'.format(self.id)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)],
                                        default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    Interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Product {}'.format(self.id)

    def refill(self):
        self.stock += 100
        self.save()


class Client(User):
    PROVINCE_CHOICES = [('AB', 'Alberta'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'), ]

    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)
    company = models.CharField(max_length=50, blank=True)
    user_image = models.ImageField(upload_to='user_image/', blank=True, null=True)

    def __str__(self):
        return 'Client {}'.format(self.id)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField()
    VALID_VALUES = [(0, 'Order Cancelled'), (1, 'Order Placed'), (2, 'OrderShipped'), (3, 'Order Delivered')]
    order_status = models.IntegerField(default=1, choices=VALID_VALUES)
    status_date = models.DateField(null=True)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def total_cost(self):
        pass
