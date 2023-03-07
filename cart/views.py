from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views import generic
from eshop.models import Product
from .carts import Cart
# Create your views here.

class AddToCard(generic.View):
    def get(self, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('product_id'))
        cart = Cart(self.request)
        cart.update(product.id, 1)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
    
