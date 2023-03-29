from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from .forms import CheckoutForm

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
            return JsonResponse({
                'success': True,
                'errors': None
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors)
            })