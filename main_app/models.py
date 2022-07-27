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

class Category(models.Model):
    # name of the category
    name = models.CharField(
        max_length=255,
        db_index=True
    )
    # slug is used to create a URL for the category
    #  e.g. /categories/<slug>/ (slug is the name of the category)
    # unique=True means that the slug is unique
    slug = models.SlugField(
        max_length=255,
        unique=True
    )
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
        return f"{S3_BASE_URL}{BUCKET}/{self.url}"
    
class Reviews(models.Model):
    # many reviews can belong to one product
    # build a link between the product and the review
    #   on_delete=models.CASCADE means that if the product is deleted, the review will be deleted
    #   related_name='reviews' means that the reviews will be linked to the product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    rating = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f"{self.title} - {self.user}"

class Orders(models.Moodel):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered_date_updated = models.DateTimeField(auto_now=True)
    ordered_by = models.CharField(max_length=50)
    ordered_address = models.CharField(max_length=100)
    ordered_city = models.CharField(max_length=50)
    ordered_state = models.CharField(max_length=50)
    ordered_zip = models.CharField(max_length=10)
    ordered_phone = models.CharField(max_length=10)
    ordered_email = models.EmailField()
    ordered_total = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_status = models.CharField(max_length=50)

    def __str__(self):
        return str(self.order_id)

    def get_absolute_url(self):
        return reverse('orders:detail', kwargs={'pk': self.pk})

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.price
        return total
