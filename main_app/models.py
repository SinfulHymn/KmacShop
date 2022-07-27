from email.mime import image
from tabnanny import verbose
from unicodedata import category
from venv import create
from django.db import models
from django.conf import settings
from django.urls import reverse
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'ecommerce-keys-u32'

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager,self).get_queryset().filter(is_active=True)


# Create your models here.
class Category(models.Model):
    # name of the category
    name = models.CharField(max_length=255, db_index=True)
    # slug is used to create a URL for the category
    #  e.g. /categories/<slug>/ (slug is the name of the category)
    # unique=True means that the slug is unique
    slug = models.SlugField(max_length=255, unique=True)
    
    # meta class is used to set the name of the table in the database
    class Meta:
        # sets the name of the table in the database to 'categories'
        verbose_name_plural = 'categories'
    
    def get_absolute_url(self):
        return reverse("main_app:catergory_index", args=[self.slug])
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    # many products can belong to one category
    # build a link between the category and the product
    # on_delete=models.CASCADE means that if the category is deleted, the product will be deleted
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='product_creator', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # stock of the product
    # stock = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()
    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)
        index_together = [['id', 'slug']]
    
    def get_absolute_url(self):
        return reverse('main_app:product_detail', args=[self.slug])
    
    def get_product_url(self):
        return reverse('main_app:category_products', args=[self.category.slug, self.slug])
    
    
    def get_image_url(self):
        if self.image:
            return f"{S3_BASE_URL}{BUCKET}/{self.image}"
        return None
    
    def __str__(self):
        return f"{self.name} - {self.category}"
    
# photos for the product
class ProductImage(models.Model):
    # many photos can belong to one product
    # build a link between the product and the photo
    #   on_delete=models.CASCADE means that if the product is deleted, the photo will be deleted
    #   related_name='photos' means that the photos will be linked to the product
    url = models.ImageField(upload_to='images/', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"image for product {self.product.name} - {self.url}"