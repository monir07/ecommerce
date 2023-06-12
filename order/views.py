import uuid
import json
from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.contrib import messages
from .forms import CheckoutForm
from cart.carts import Cart
from cart.models import Coupon
from .models import OrderItem, Order, SizeOptions, ColorOptions
from eshop.models import Product

# Create your views here.
class CheckoutView(generic.View):
    title = "Checkout Form"
    form_class = CheckoutForm
    template_name = 'eshop/checkout/checkout.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {
            'form': form,
            'title': self.title,
        }
        return render(request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            customer_information = form.cleaned_data
            cart = Cart(self.request)
            coupon_id = cart.coupon
            user_cart = Cart(self.request).cart
            products = Product.objects.filter(id__in=list(user_cart))
            ordered_products = []

            for product in products:
                order_item = OrderItem.objects.create(
                    product = product,
                    price = product.price,
                    quantity = user_cart[str(product.id)]['quantity'],
                    size = SizeOptions.L,
                    color = ColorOptions.BLACK,
                )
                ordered_products.append(order_item)
            order = Order.objects.create(
                user = self.request.user,
                # order_items = ordered_products,
                transaction_id = uuid.uuid4().hex,
                status = 'Received',
                total = cart.grand_total(),
                **customer_information
            )
            if coupon_id:
                order.coupon = Coupon.objects.get(id=coupon_id)

            order.order_items.add(*ordered_products)
            order.save()
            cart.clear()
            messages.success(self.request, "Order added successfully")
            return JsonResponse({
                'success': True,
                'errors': None
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors)
            })