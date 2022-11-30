import django
from myapp.models import Product, Category, Client, Order

#1.
all_products = Product.objects.all().values()
all_clients = Client.objects.all().values()
all_orders = Order.objects.all().values()

print(all_products)
print(all_clients)
print(all_orders)


