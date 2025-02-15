from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    is_featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')

    def __str__(self):
        return self.name

    def get_price(self):
        return self.price


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()  # Elimina auto_now_add=True
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Compra {self.id} - {self.client.name}"

    def update_total(self):
        self.total = self.purchasedetail_set.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
        self.save()


class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.product.get_price() * self.quantity
        super().save(*args, **kwargs)
        self.purchase.update_total()
