from django import forms
from .models import Phone


class CreateForm(forms.Form):
    brand_name = forms.CharField(max_length=200)
    brand_nation = forms.CharField(max_length=200)
    model_name = forms.CharField(max_length=200)
    color = forms.CharField(max_length=200)
    price = forms.IntegerField()
    screen_size = forms.FloatField()
    region = forms.CharField(max_length=200)
    inventory_status = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

    def clean_model_name(self):
        model_name = self.cleaned_data['model_name']
        if Phone.objects.filter(model_name__iexact=model_name).exists():
            raise forms.ValidationError("A phone with this model name already exist !")
        return model_name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be a positive number.")
        return price

    def clean_screen_size(self):
        screen_size = self.cleaned_data.get('screen_size')
        if screen_size is not None and screen_size <= 0:
            raise forms.ValidationError("Screen size must be a positive number.")
        return screen_size


class PhoneFilterForm(forms.Form):
    INVENTORY_STATUS_CHOICES = [
        ('', 'Any'),
        ('available', 'Available'),
        ('unavailable', 'Unavailable')
    ]
    brand_name = forms.CharField(required=False)
    brand_nation = forms.CharField(required=False)
    model_name = forms.CharField(required=False)
    color = forms.CharField(required=False)
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)
    min_screen_size = forms.FloatField(required=False)
    max_screen_size = forms.FloatField(required=False)
    region = forms.CharField(required=False)
    inventory_status = forms.ChoiceField(choices=INVENTORY_STATUS_CHOICES, required=False)

    def clean_inventory_status(self):
        inventory_status = self.cleaned_data.get('inventory_status')
        if inventory_status == '':
            return None
        return inventory_status


class UpdateForm(forms.Form):
    brand_name = forms.CharField(max_length=200)
    brand_nation = forms.CharField(max_length=200)
    model_name = forms.CharField(max_length=200)
    color = forms.CharField(max_length=200)
    price = forms.IntegerField()
    screen_size = forms.FloatField()
    region = forms.CharField(max_length=200)
    inventory_status = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be a positive number.")
        return price

    def clean_screen_size(self):
        screen_size = self.cleaned_data.get('screen_size')
        if screen_size is not None and screen_size <= 0:
            raise forms.ValidationError("Screen size must be a positive number.")
        return screen_size
