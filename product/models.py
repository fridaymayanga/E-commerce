from django.db import models
import uuid
from autheticate.models import User

# Create your models here.

class ProductAlbum(models.Model):
    id = models.UUIDField(default = uuid.uuid4,primary_key=True, editable=False)
MEDIA_TYPE =[
    ("IMAGE","image"),
    ("VIDEO","video")
    ]
class Media(models.Model):
    album = models.ForeignKey(ProductAlbum, on_delete = models.CASCADE,related_name= "album")
    id = models.UUIDField(default = uuid.uuid4,primary_key=True, editable=False)
    file = models.FileField(upload_to="product")
    type = models.CharField(max_length = 5, choices= MEDIA_TYPE, default= MEDIA_TYPE[0][0])
class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name =models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    quantity_sold = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(decimal_places=2, max_digits=5)
    album = models.ForeignKey(ProductAlbum, on_delete=models.SET_NULL, null=True, blank=True, related_name="product_ablum")
    expire_at = models.DateField(null=True, blank=True)
    created_at = models. DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User,on_delete= models.CASCADE, related_name= "products")
    updated_at = models.DateTimeField(auto_now=True)
    
# Create your models here.

class Sale(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True,editable=False)
    total_amount = models.PositiveIntegerField()
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    editable_at = models.DateTimeField(auto_now=True)

class ProductSale(models.Model):
        id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
        product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_sale_record")
        sale = models.ForeignKey(Sale, on_delete=models.CASCADE,related_name="sale_product")
        quantity = models.PositiveIntegerField ()
        price = models.PositiveIntegerField ()