from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    address = models.CharField(max_length=256, blank=True, null=True)
    removed = models.BooleanField(default=False, blank=False, null=False)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    img = models.ImageField(upload_to='product_images/%Y/%m/%d/', blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f'{self.product}'


class Comment(models.Model):
    comment = models.TextField(blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f'{self.product}'


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    date_create = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f'{self.user}'


class UserAccount(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    phone = models.CharField(max_length=16, blank=False, null=False)

    def __str__(self):
        return f'{self.account}'

