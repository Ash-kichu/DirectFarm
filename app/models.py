from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('Farmer', 'Farmer'),
        ('Customer', 'Customer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    location = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    farm_name = models.CharField(max_length=100, blank=True, null=True)
    farm_description = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='farmer_profiles/', blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    offer_percentage = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    description = models.TextField()
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
    category = models.CharField(max_length=50, choices=PRODUCT_CATEGORIES, default='Others')
    availability = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField()
    farmer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.farmer.user_type != 'Farmer':
            raise ValueError("Only users of type 'Farmer' can create products.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart of {self.user.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} in cart of {self.cart.user.user.username}"

class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash on Delivery', 'Cash on Delivery'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    payment_status = models.CharField(max_length=20, default='Pending')
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} in order {self.order.id}"

