from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg
from .models import Watch, Brand, Category, Review
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def home(request):
    featured = Watch.objects.filter(is_featured=True, is_active=True)[:8]
    new_arrivals = Watch.objects.filter(is_new_arrival=True, is_active=True)[:8]
    bestsellers = Watch.objects.filter(is_bestseller=True, is_active=True)[:8]
    brands = Brand.objects.all()[:6]
    categories = Category.objects.all()

    context = {
        'featured': featured,
        'new_arrivals': new_arrivals,
        'bestsellers': bestsellers,
        'brands': brands,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def watch_list(request):
    watches = Watch.objects.filter(is_active=True)
    brands = Brand.objects.all()
    categories = Category.objects.all()

    # Filters
    brand_slug = request.GET.get('brand')
    category_slug = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', 'newest')

    if brand_slug:
        watches = watches.filter(brand__slug=brand_slug)
    if category_slug:
        watches = watches.filter(category__slug=category_slug)
    if min_price:
        watches = watches.filter(price__gte=min_price)
    if max_price:
        watches = watches.filter(price__lte=max_price)

    if sort == 'price_low':
        watches = watches.order_by('price')
    elif sort == 'price_high':
        watches = watches.order_by('-price')
    elif sort == 'name':
        watches = watches.order_by('name')
    elif sort == 'rating':
        watches = watches.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        watches = watches.order_by('-created_at')

    context = {
        'watches': watches,
        'brands': brands,
        'categories': categories,
        'current_brand': brand_slug,
        'current_category': category_slug,
        'current_sort': sort,
        'min_price': min_price or '',
        'max_price': max_price or '',
    }
    return render(request, 'store/watch_list.html', context)


def watch_detail(request, slug):
    watch = get_object_or_404(Watch, slug=slug, is_active=True)
    related = Watch.objects.filter(brand=watch.brand, is_active=True).exclude(pk=watch.pk)[:4]
    reviews = watch.reviews.all()[:10]
    user_reviewed = False
    if request.user.is_authenticated:
        user_reviewed = Review.objects.filter(watch=watch, user=request.user).exists()

    context = {
        'watch': watch,
        'related': related,
        'reviews': reviews,
        'user_reviewed': user_reviewed,
    }
    return render(request, 'store/watch_detail.html', context)


def search(request):
    query = request.GET.get('q', '')
    watches = Watch.objects.filter(is_active=True)
    if query:
        watches = watches.filter(
            Q(name__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    context = {
        'watches': watches,
        'query': query,
    }
    return render(request, 'store/search_results.html', context)


@login_required
@require_POST
def add_review(request, slug):
    watch = get_object_or_404(Watch, slug=slug)
    if Review.objects.filter(watch=watch, user=request.user).exists():
        return JsonResponse({'error': 'You have already reviewed this watch'}, status=400)

    rating = int(request.POST.get('rating', 5))
    title = request.POST.get('title', '')
    comment = request.POST.get('comment', '')

    Review.objects.create(
        watch=watch,
        user=request.user,
        rating=rating,
        title=title,
        comment=comment,
    )
    return JsonResponse({'success': True, 'message': 'Review added successfully!'})
