from typing import Any
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CategoryModel(BaseModel):
    title = models.CharField(max_length=70, unique=True)
    slug = models.SlugField(blank=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductModel(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    discount = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='product')
    is_liked = models.ManyToManyField(User, related_name='liked_products', blank=True)

    objects = models.Manager()

    @property
    def discounted_price(self) -> Any:
        if self.discount > 0:
            return self.price * (1 - (self.discount / 100.0))
        return self.price

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class ImageModel(BaseModel):
    is_primary = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/products/')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class CommentModel(BaseModel):
    class Rating(models.IntegerChoices):
        One = 1
        Two = 2
        Three = 3
        Four = 4
        Five = 5

    message = models.TextField()
    rating = models.IntegerField(choices=Rating.choices, default=Rating.One.value)
    file = models.FileField(null=True, blank=True, upload_to='comments/')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class KeyModel(BaseModel):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Key'
        verbose_name_plural = 'Keys'


class ValueModel(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Value'
        verbose_name_plural = 'Values'


class AttributeModel(models.Model):
    key = models.ForeignKey(KeyModel, on_delete=models.CASCADE)
    value = models.ForeignKey(ValueModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='attributes')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'
