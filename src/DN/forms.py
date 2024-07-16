from django import forms
from .models import delivery,orders

class DateInput(forms.DateInput):
    input_type = 'date'

class DeliveryForm(forms.ModelForm):
    delivery_number = forms.IntegerField(required=True)
    class Meta:
        model = delivery
        fields = ['serial_no','delivery_number','delivery_date', 'delivery_quantity','truck_number','driver_name','recipient_name','delivery_comment']

class OrderForm(forms.ModelForm):
    class Meta:
        model = orders
        fields = ['serial_no','customer_name','date','invoice', 'description', 'price','order_quantity','invoice_type','total_price','before_vat','comment','measurement','withholding_amount']
        