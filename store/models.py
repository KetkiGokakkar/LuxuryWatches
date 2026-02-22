from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:watch_list') + f'?brand={self.slug}'


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Watch(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='watches')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='watches')
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    original_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='watches/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='watches/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='watches/', blank=True, null=True)

    # Specifications
    case_material = models.CharField(max_length=200, blank=True)
    case_diameter = models.CharField(max_length=50, blank=True)
    movement = models.CharField(max_length=200, blank=True)
    water_resistance = models.CharField(max_length=100, blank=True)
    strap_material = models.CharField(max_length=200, blank=True)
    dial_color = models.CharField(max_length=100, blank=True)
    crystal = models.CharField(max_length=100, blank=True)
    power_reserve = models.CharField(max_length=100, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)

    stock = models.IntegerField(default=10)
    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Watches'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand.name} {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand.name}-{self.name}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:watch_detail', kwargs={'slug': self.slug})

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    @property
    def avg_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return round(sum(r.rating for r in reviews) / len(reviews), 1)
        return 0

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def in_stock(self):
        return self.stock > 0


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('watch', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.watch.name} ({self.rating}★)"


class Wishlist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='wishlist')
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'watch')

    def __str__(self):
        return f"{self.user.username} - {self.watch.name}"
