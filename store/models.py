from django.db import models

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
        managed = False


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    is_main = models.BooleanField(default=False)

    class Meta:
        db_table = "product_images"
        managed = False

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = "users"
        managed = False

class address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    address= models.TextField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "address"
        managed = False


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    category_image = models.ImageField(upload_to='media/category_images/', null=True, blank=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "categories"
        managed = False

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField()

    class Meta:
        db_table = "cart"
        managed = False

class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    liked_at = models.DateTimeField()

    class Meta:
        db_table = "likes"
        managed = False

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