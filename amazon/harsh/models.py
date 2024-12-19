from django.db import models
from django.contrib.auth.models import User
# Create your models here.
STATE_CHOICES=(
    ('MH','MH'),
    ('UP','UP'),
    ('MP','MP'),
    ('J&K','J&K'),
)

class Customer(models.Model):
    customer=models.ForeignKey(User, on_delete=models.CASCADE)
    Full_name=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(choices=STATE_CHOICES, max_length=10)
    mobile=models.PositiveIntegerField()
    def __str__(self):
        return str(self.Full_name)

CATEGORY=(
    ('fashion','fashion'),
    ('household','household'),
    ('mobile','mobile'),
    ('laptop','laptop'),
    ('watches','watches')
)
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    category=models.CharField(choices=CATEGORY, max_length=20)
    brand=models.CharField(max_length=20)
    pic=models.ImageField(upload_to='pics')
    def __str__(self):
        return str(self.title)

class Cart(models.Model):
    user=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.user)

class Orders(models.Model):
    user=models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='order_by')
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='customer_pro')
    
