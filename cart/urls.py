from django.urls import path
from .views import AddToCard
urlpatterns = [
    path('add-cart/<int:product_id>', AddToCard.as_view(), name='add_to_cart'),
]
