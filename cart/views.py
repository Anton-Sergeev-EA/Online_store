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
    
    # Проверяем наличие товара
    if product.get_available_quantity() <= 0:
        messages.error(request, 'Товар временно отсутствует на складе')
        return redirect('product_detail', slug=product.slug)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart,
                                                        product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request,
                         f'Количество товара "{product.name}" увеличено')
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
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            return remove_from_cart(request, product_id)
        
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request,
                             f'Количество товара "{product.name}" обновлено')
        except CartItem.DoesNotExist:
            messages.error(request, 'Товар не найден в корзине')
    
    return redirect('cart:cart_view')
