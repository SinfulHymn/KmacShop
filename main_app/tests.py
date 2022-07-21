

# Create your tests here.
from email.mime import image
from unicodedata import category
from django.contrib.auth.models import User
from django.test import TestCase

from main_app.models import Category, Product

class TestCategoriesModel(TestCase):
    
    def setUp(self):
        self.data1 = Category.objects.create(name='test-category', slug='test-category')
        # print('~~~~id12312',self.data1.id)
    
    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        
        data = self.data1
        self.assertTrue(isinstance(data, Category))
    
    def test_category_model_name(self):
        """
        Test Category model data name
        """
        data = self.data1

        self.assertEqual(str(data), 'test-category')
class TestProductsModel(TestCase):
    def setUp(self):
        test = Category.objects.create(name='test-category', slug='test-category')
        print('~~~~id12312',test.id)
        User.objects.create(username='admin') 
        self.data1 = Product.objects.create(category_id=3, title='test-product', created_by_id=1, description='test-description', price=10.00, slug='test-product', image='test-image')
           
    def test_products_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        # print(data.title, "123123")
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'test-product')