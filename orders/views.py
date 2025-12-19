from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem
from products.models import Stock


@login_required
def create_order(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Ваша корзина пуста')
        return redirect('cart:cart_view')

    if not cart.items.exists():
        messages.error(request, 'Ваша корзина пуста')
        return redirect('cart:cart_view')

    # Проверяем наличие всех товаров.
    for item in cart.items.all():
        if item.quantity > item.product.get_available_quantity():
            messages.error(request, f'Товара "{item.product.name}" недостаточно на складе')
            return redirect('cart:cart_view')

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address', '')

        if not shipping_address:
            messages.error(request, 'Пожалуйста, укажите адрес доставки')
            return render(request, 'orders/order_form.html', {'cart': cart})

        try:
            with transaction.atomic():
                # Создаем заказ.
                order = Order.objects.create(
                    user=request.user,
                    total_amount=cart.total_price,
                    shipping_address=shipping_address
                )

                # Создаем элементы заказа и резервируем товары.
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )

                    # Резервируем товар.
                    stock = Stock.objects.get(product=cart_item.product)
                    stock.reserved += cart_item.quantity
                    stock.save()

                # Очищаем корзину.
                cart.items.all().delete()

                messages.success(request, f'Заказ #{order.id} успешно создан!')
                return redirect('orders:order_detail', order_id=order.id)

        except Exception as e:
            messages.error(request, f'Произошла ошибка при создании заказа: {str(e)}')

    return render(request, 'orders/order_form.html', {'cart': cart})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Пагинация.
    paginator = Paginator(orders, 30)  # 30 заказов на страницу.
    page = request.GET.get('page')

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return render(request, 'orders/order_history.html', {
        'orders': orders,
        'paginator': paginator,
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
