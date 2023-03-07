from django import forms
from .models import QueryMessage
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ContactUsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()    
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Message'))
    class Meta:
        model = QueryMessage
        fields = '__all__'