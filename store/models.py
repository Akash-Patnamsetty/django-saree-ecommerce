from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    stock_quantity = models.IntegerField(default=0)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
    'Category',
    on_delete=models.CASCADE,
    db_column='category_id'
)

    class Meta:
        db_table = "products"
        


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    is_main = models.BooleanField(default=False)

    class Meta:
        db_table = "product_images"
       

# class Users(models.Model):
#     id = models.AutoField(primary_key=True)
#     full_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=15, unique=True)
#     password = models.CharField(max_length=255)
#     date_joined = models.DateTimeField()
#     last_login = models.DateTimeField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     class Meta:
#         db_table = "users"

class Users(models.Model):
    ROLE_CUSTOMER = "customer"
    ROLE_STAFF = "staff"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = [
        (ROLE_CUSTOMER, "Customer"),
        (ROLE_STAFF, "Staff"),
        (ROLE_ADMIN, "Admin"),
    ]

    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # NEW FIELDS
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_CUSTOMER,
    )
    must_change_password = models.BooleanField(default=False)

    class Meta:
        db_table = "users"

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff_member(self):
        return self.role in (self.ROLE_STAFF, self.ROLE_ADMIN)
        
        
        
        
        
        

class address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    address= models.TextField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "address"
       


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    category_image = models.ImageField(upload_to='media/category_images/', null=True, blank=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "categories"
        

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField()

    class Meta:
        db_table = "cart"
        

class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    liked_at = models.DateTimeField()

    class Meta:
        db_table = "likes"
        

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    address_id = models.IntegerField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    payment_status = models.CharField(max_length=20, default="Pending")
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"
class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "order_items"
        
        
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id', related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id', related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    headline = models.CharField(max_length=150)
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reviews"
        ordering = ["-created_at"]
        unique_together = ("user", "product") 