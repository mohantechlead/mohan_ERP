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
        fields = ['serial_no','delivery_number','delivery_date','truck_number','driver_name','recipient_name','delivery_comment']
        
class DeliverItemForm(forms.ModelForm):
    description = forms.ModelChoiceField(
        queryset=finished_goods.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),)
    
    no_of_unit = forms.FloatField(
        required = False,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add No of Units', 'id':'no_of_unit'})
    )

    UNIT_CHOICES =( 
        ("", ""),
    ("Bag", "Bag"), 
    ("Pkg", "Pkg"),
    ("Crt", "Crt"),) 
    
    unit_type = forms.ChoiceField(
        choices = UNIT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        
    )
    per_unit_kg = forms.FloatField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add value of KG per Unit', 'id': 'per_unit_kg'})
    )
        
    quantity = forms.IntegerField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantity',  'id':'quantity', 'readonly':'readonly'})
    )
    
    Measurement_unit_choices =( 
        ("", ""),
    ("kgs", "kgs")) 

    measurement_unit = forms.ChoiceField(
        choices = Measurement_unit_choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        
    )
    remark = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add No of Units', 'id':'no_of_unit'})
    )
    
    class Meta:
        model = orders_items
        fields = ['description', 'no_of_unit', 'unit_type','per_unit_kg', 'quantity', 'measurement_unit']


class OrderItemForm(forms.ModelForm):
    description = forms.ModelChoiceField(
        queryset=finished_goods.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),)
    
    no_of_unit = forms.FloatField(
        required = False,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add No of Units', 'id':'no_of_unit'})
    )

    UNIT_CHOICES =( 
        ("", ""),
    ("Bag", "Bag"), 
    ("Pkg", "Pkg"),
    ("Crt", "Crt"),) 
    
    unit_type = forms.ChoiceField(
        choices = UNIT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        
    )
    per_unit_kg = forms.FloatField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add value of KG per Unit', 'id': 'per_unit_kg'})
    )
        
    quantity = forms.IntegerField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantity',  'id':'quantity', 'readonly':'readonly'})
    )
    
    unit_price = forms.FloatField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'unit_price',  'id':'unit_price'})
    )
    
    total_price = forms.FloatField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price',  'id':'total_price','readonly':'readonly'})
    )
    
    Measurement_unit_choices =( 
        ("", ""),
    ("kgs", "kgs")) 

    measurement_unit = forms.ChoiceField(
        choices = Measurement_unit_choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        
    )
    class Meta:
        model = orders_items
        fields = ['description', 'unit_price', 'no_of_unit', 'unit_type','per_unit_kg', 'quantity', 'measurement_unit', 'total_price']

class OrderForm(forms.ModelForm):
    class Meta:
        model = orders
        fields = ['serial_no','customer_name','date','invoice', 'final_price','invoice_type','before_vat','withholding_amount','vat_amount','reciveable']
        