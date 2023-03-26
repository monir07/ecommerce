from django.urls import path, include
from .views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product-list/', ProductListView.as_view(), name='product_list'),
    path('product-details/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('contact-us/', ContactUsCreateView.as_view(), name='contact_us_create'),
]