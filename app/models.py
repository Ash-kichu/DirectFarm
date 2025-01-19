from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class Farmer(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='farmer_profile',
    )
    phone = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.TextField()
    location = models.CharField(max_length=100)
    farm_name = models.CharField(max_length=100)
    farm_description = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='farmer_profiles/', blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
class Product(models.Model):
    PRODUCT_CATEGORIES = [
        ('Vegetables', 'Vegetables'),
        ('Fruits', 'Fruits'),
        ('Grains', 'Grains'),
        ('Dairy', 'Dairy'),
        ('Honey', 'Honey'),
        ('Oil', 'Oil'),
        ('Eggs', 'Eggs'),
        ('Others', 'Others'),
    ]
    
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=PRODUCT_CATEGORIES, default='Others')
    availability = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField()
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
