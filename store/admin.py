from django.contrib import admin
from .models import Brand, Category, Watch, Review, Wishlist


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'founded_year']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'stock', 'is_featured', 'is_active']
    list_filter = ['brand', 'category', 'is_featured', 'is_new_arrival', 'is_bestseller', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'brand__name', 'description']
    list_editable = ['is_featured', 'is_active', 'stock']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['watch', 'user', 'rating', 'created_at']
    list_filter = ['rating']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'watch', 'added_at']
