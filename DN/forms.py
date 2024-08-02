from django import forms
from .models import *
from FGRN.models import finished_goods

class DateInput(forms.DateInput):
    input_type = 'date'
    description = forms.ModelChoiceField(
        queryset=finished_goods.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),)

class DeliveryForm(forms.ModelForm):
    delivery_number = forms.IntegerField(required=True)
    class Meta:
        model = delivery
        fields = ['serial_no','delivery_number','delivery_date', 'delivery_quantity','truck_number','driver_name','recipient_name','delivery_comment']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = orders_items
        fields = ['description', 'no_of_unit', 'unit_type', 'order_quantity', 'price_per_kg', 'price', 'order_quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = orders
        fields = ['serial_no','customer_name','date','invoice', 'total_price','invoice_type','before_vat','withholding_amount']
        