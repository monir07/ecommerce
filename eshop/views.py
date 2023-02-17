from django.shortcuts import render
from django.views import View, generic

# Create your views here.
class HomeView(generic.TemplateView):
    template_name = 'eshop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = 'ecommerce'
        return context