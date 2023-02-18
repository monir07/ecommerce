import csv
import requests
from django.core.management import BaseCommand
from django.utils.text import slugify
from eshop.models import (Category, Product, ProductStock)
from django.contrib.auth import get_user_model
User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("createing Data.....")
        success_record = 0
        response = requests.get('https://fakestoreapi.com/products').json()
        user_obj = User.objects.get(username='admin')
        product_list = [["catetory", "title", "price", "image", "description"]]
        for product in response:
            print(product["id"])
            product_list.append([ product["category"], product["title"], product["price"], product["image"], product["description"]])
            with open('product_list.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(product_list)
                
            """ 
            category, _ = Category.objects.get_or_create(
                title = product["category"][:150],
                slug = slugify(product["category"][:150]),
                featured = True,
                created_by = user_obj
            )
            product_obj = Product.objects.create(
                category =category,
                title =product["title"][:150],
                slug = slugify(product["title"][:150]),
                price = product["price"],
                thumbnail = product["image"],
                description = product["description"][:250],
                created_by = user_obj
            )
            ProductStock.objects.create(
                product = product_obj,
                stock_count = 20,
            )
            """
            success_record += 1
        print(f"Insertion Complete: {success_record} Nos.")
