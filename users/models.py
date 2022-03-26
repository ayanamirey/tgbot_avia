from django.db import models

lang_choice = (
    ('uz', 'Uzbek'),
    ('ru', 'Russian')
)


def upload_to(instance, filename):
    return 'product_imgs/{filename}'.format(filename=filename)


class User(models.Model):
    chat_id = models.CharField(max_length=50)
    fullname = models.CharField(max_length=50, null=True)
    contact_number = models.CharField(max_length=20, null=True)
    lang = models.CharField(max_length=2, choices=lang_choice, null=True)
    departure = models.CharField(max_length=50, null=True)
    arrival = models.CharField(max_length=50, null=True)
    verify = models.BooleanField(default=False)
    sms_code = models.CharField(max_length=6, null=True)


class Category(models.Model):
    title = models.CharField(max_length=50)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to=upload_to, null=True)
    price = models.FloatField()
    description = models.TextField(null=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    total_price = models.FloatField(null=True)
    location = models.JSONField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateField(auto_now_add=True)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()


class Region(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    soato_code = models.IntegerField(null=True)
    title = models.CharField(max_length=100)


class Branch(models.Model):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    location = models.JSONField(null=True)
    contact_number = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True)
