from django.db import transaction
from django.db.models import Q, Prefetch, Sum, Value
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
import datetime
from .models import Product, ProductStock, QueryMessage
from .forms import ContactUsForm
from cart.carts import Cart

def format_search_string(fields, keyword):
    Qr = None
    for field in fields:        
        q = Q(**{"%s__icontains" % field: keyword })
        if Qr:
            Qr = Qr | q
        else:
            Qr = q
    
    return Qr


# Create your views here.
class HomeView(generic.TemplateView):
    template_name = 'eshop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = 'ecommerce'
        return context


class ProductListView(generic.ListView):
    permission_required = 'eshop.view_product'
    model = Product
    context_object_name = 'items'
    paginate_by = 9
    template_name = 'eshop/shop.html'
    queryset = Product.objects.all()
    search_fields = ['title', 'category__title']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_count'] = self.get_queryset().count()
        context['basic_template'] = ""
        return context


class ProductDetailView(generic.DetailView):
    permission_required = 'eshop.view_product'
    model = Product
    context_object_name = 'item'
    template_name = 'eshop/detail.html'
    # queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_count'] = self.get_queryset().count()
        context['basic_template'] = ""
        return context


class ContactUsCreateView(generic.CreateView):
    model = QueryMessage
    form_class = ContactUsForm
    template_name = 'eshop/contact.html'
    success_message = "Message Sent Success."
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        with transaction.atomic():
            self.object.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ""
        return context


class ShopingCartListView(generic.ListView):
    permission_required = 'eshop.view_product'
    model = Product
    context_object_name = 'items'
    paginate_by = 9
    template_name = 'eshop/cart.html'
    queryset = Product.objects.all()
    search_fields = ['title', 'category__title']
    """ 
    def get(self, request, *args, **kwargs):
        cart_items = Cart(self.request)
        print(cart_items.cart)
        return super().get(request, *args, **kwargs)
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        
        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)

        return queryset