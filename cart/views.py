from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Проверяем текущее количество товара в корзине пользователя.
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        current_quantity_in_cart = cart_item.quantity
    except CartItem.DoesNotExist:
        current_quantity_in_cart = 0

    # Проверяем общее доступное количество товара.
    available_quantity = product.get_available_quantity()

    # Если пользователь пытается добавить больше, чем есть в наличии.
    if current_quantity_in_cart + 1 > available_quantity:
        if available_quantity <= 0:
            messages.error(request, 'Товар временно отсутствует на складе')
        else:
            messages.error(request, f'Доступно только {available_quantity} шт. товара "{product.name}"')
        return redirect('products:product_detail', slug=product.slug)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Количество товара "{product.name}" увеличено')
    else:
        messages.success(request, f'Товар "{product.name}" добавлен в корзину')

    return redirect('cart:cart_view')


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        messages.success(request, f'Товар "{product.name}" удален из корзины')
    except CartItem.DoesNotExist:
        messages.error(request, 'Товар не найден в корзине')

    return redirect('cart:cart_view')


@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = get_object_or_404(Cart, user=request.user)

        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            messages.error(request, 'Некорректное количество')
            return redirect('cart:cart_view')

        if quantity <= 0:
            return remove_from_cart(request, product_id)

        # Проверяем доступность товара.
        available_quantity = product.get_available_quantity()

        # Учитываем количество, которое уже есть в корзине у других пользователей,
        # но для текущего пользователя проверяем только доступное общее количество.
        if quantity > available_quantity:
            messages.error(request, f'Доступно только {available_quantity} шт. товара "{product.name}"')
            return redirect('cart:cart_view')

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f'Количество товара "{product.name}" обновлено')
        except CartItem.DoesNotExist:
            messages.error(request, 'Товар не найден в корзине')

    return redirect('cart:cart_view')
