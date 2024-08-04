from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='phones')
    model_name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=200)
    screen_size = models.FloatField()
    price = models.PositiveIntegerField()
    region = models.CharField(max_length=200)
    inventory_status = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return f"{self.brand.brand_name} {self.model_name}"

    def save(self, *args, **kwargs):
        if not self.slug:

            self.slug = slugify(f"{self.brand.brand_name}-{self.model_name}")
        super().save(*args, **kwargs)


class Brand(models.Model):
    brand_name = models.CharField(max_length=200, unique=True)
    brand_nation = models.CharField(max_length=200)

    def __str__(self):
        return self.brand_name
