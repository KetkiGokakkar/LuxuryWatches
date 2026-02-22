from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem, Order, OrderItem
from store.models import Watch
from accounts.models import Address
from decimal import Decimal


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_view(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('watch', 'watch__brand')
    context = {'cart': cart, 'items': items}
    return render(request, 'cart/cart.html', context)


@require_POST
def add_to_cart(request, watch_id):
    watch = get_object_or_404(Watch, pk=watch_id, is_active=True)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, watch=watch)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'message': f'{watch.name} added to cart!'
        })
    messages.success(request, f'{watch.brand.name} {watch.name} added to cart!')
    return redirect('cart:cart')


@require_POST
def update_cart(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        item.delete()
    else:
        item.quantity = quantity
        item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'subtotal': str(cart.subtotal),
            'tax': str(cart.tax),
            'total': str(cart.total),
            'line_total': str(item.line_total) if quantity > 0 else '0',
        })
    return redirect('cart:cart')


def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart:cart')


@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('watch', 'watch__brand')

    if not items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart')

    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        if not address_id:
            messages.error(request, 'Please select a delivery address.')
            return redirect('cart:checkout')

        address = get_object_or_404(Address, pk=address_id, user=request.user)

        subtotal = cart.subtotal
        tax = Decimal(str(cart.tax))
        total = Decimal(str(cart.total))

        order = Order.objects.create(
            user=request.user,
            full_name=address.full_name,
            email=request.user.email,
            phone=address.phone,
            address_line1=address.address_line1,
            address_line2=address.address_line2,
            city=address.city,
            state=address.state,
            postal_code=address.postal_code,
            country=address.country,
            subtotal=subtotal,
            tax=tax,
            total=total,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                watch=item.watch,
                watch_name=f"{item.watch.brand.name} {item.watch.name}",
                watch_brand=item.watch.brand.name,
                price=item.watch.price,
                quantity=item.quantity,
            )
            item.watch.stock -= item.quantity
            item.watch.save()

        cart.items.all().delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('cart:order_confirmation', order_number=order.order_number)

    context = {
        'cart': cart,
        'items': items,
        'addresses': addresses,
    }
    return render(request, 'cart/checkout.html', context)


@login_required
def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'cart/order_confirm.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'cart/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'cart/order_detail.html', {'order': order})
