from enum import unique
from django.db import models


# +----------------+        +----------------------+        +----------------+
# |   Category     |◄───────┤    ClothingItem      ├───────┬►   Size         |
# |----------------|        |----------------------|       |----------------|
# | id (PK)        |        | id (PK)              |       | id (PK)        |
# | name           |        | name                 |       | name           |
# | slug           |        | slug                 |       +----------------+
# +----------------+        | category_id (FK) ◄───┘
#                           | ... (price, desc)    |
#                           +----------------------+
#                                   ▲
#                                   │
#                                   │ through
#                                   ▼
#                       +--------------------------+
#                       |   ClothingItemSize       |
#                       |--------------------------|
#                       | id (PK)                  |
#                       | clothing_item_id (FK) ───┘
#                       | size_id (FK)         ────┘
#                       | available (bool)         |
#                       +--------------------------+

                        # | id | clothing_item_id   | size_id  | available |
                        # | -- | ------------------ | -------- | --------- |
                        # | 1  | 1                  | 1        | True      |
                        # | 2  | 1                  | 2        | False     |
                        # | 3  | 1                  | 3        | True      |


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name',])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class ClothingItem(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    available = models.BooleanField(default=True)
    sizes = models.ManyToManyField(Size, through='ClothingItemSize', 
                                   related_name='clothing_item', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='clothing_items')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def get_price_with_discount(self):
        if self.discount > 0:
            return self.price * (1 - (self.discount / 100)) 
        return self.price

class ClothingItemSize(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('clothing_item', 'size')
