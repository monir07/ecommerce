from django.db import transaction
from django.db.models import Q, Prefetch, Sum, Value, Count
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
import datetime
from .models import Product, ProductStock, QueryMessage, Category
from .forms import ContactUsForm
from cart.carts import Cart
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .serializer import ProductSerializer

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
        category_list = query_param.get('category', None)
        category = category_list.split(',') if category_list else None
        if category:
            queryset = queryset.filter(Q(category__title__in=category))

        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_count'] = self.get_queryset().count()
        context['all_product_count'] = self.queryset.count()
        context['basic_template'] = ""
        context['categories'] = Category.objects.annotate(product_count=Count('products'))

        return context
    
    def get_category_list(self, **kwargs):
        queryset = Category.objects.all()
        for item in queryset:
            print(item.products.all())
        return queryset

class ProductFilterListView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, format=None):
        query_param = self.request.GET.copy()
        search_param = query_param.get('category', None).split(',')
        print(search_param)
        products = Product.objects.filter(Q(category__title__in=search_param))
        serializer = ProductSerializer(products, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)


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

