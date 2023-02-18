from django.db import models
from django.contrib.auth import get_user_model
from account.validator import image_validator
User = get_user_model()

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)ss')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT,  related_name='updated_%(class)ss', null=True, blank=True)

    class Meta:
        abstract = True

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self.__class__.__name__._meta.fields]


class Category(BaseModel):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ('title',)
    
    def __str__(self):
        return self.title


class Product(BaseModel):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(unique=True)
    featured = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(max_length=200)

    class Meta:
        ordering = ('-id',)
    
    def __str__(self):
        return self.title


class ProductStock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    stock_count = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True, editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT,  related_name='updated_%(class)ss', null=True, blank=True)

    def __str__(self):
        return f'{self.product.title} Stock ({self.stock_count})'


class Slider(BaseModel):
    title = models.CharField(max_length=50)
    banner = models.ImageField(upload_to='banners', 
                                validators=[image_validator],
                                help_text="File size should be less than 2MB with .jpeg .jpg .png .gif extension")
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.title