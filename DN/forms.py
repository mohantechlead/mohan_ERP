from django import forms
from .models import *
from FGRN.models import finished_goods
from itertools import chain
from MR.models import inventory
import operator

class DateInput(forms.DateInput):
    input_type = 'date'
    description = forms.ModelChoiceField(
        queryset=finished_goods.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),)

class DeliveryForm(forms.ModelForm):
    delivery_number = forms.IntegerField(required=True,
                                        widget = forms.TextInput(attrs={'class': 'form-control', 
                                        'type':'text',
                                        'placeholder': 'Add a Truck Number', 
                                        'id':'delivery_number'}))
    
    delivery_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select a date',
                'id':'delivery_date'
            }
        )
    )

    truck_number = forms.CharField(
        label="Truck Number",
        required=False, 
        widget = forms.TextInput(attrs={'class': 'form-control', 
                                        'type':'text',
                                        'placeholder': 'Add a Truck Number', 
                                        'id':'truck_number'}))
    
    driver_name = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={'class': 'form-control', 
                                        'placeholder': 'Add a Driver Name', 
                                        'id':'driver_name'})
                                  )
    recipient_name = forms.CharField(required=False,
                                    widget = forms.TextInput(attrs={'class': 'form-control', 
                                        'placeholder': 'Add a Recipient Name', 
                                        'id':'recipient_name'}))
    
    delivery_comment = forms.CharField(required=False,
                                       widget = forms.TextInput(attrs={
                                        'class': 'form-control', 
                                        'placeholder': 'Add a Delivery Comment', 
                                        'id':'delivery_comment'}))
    class Meta:
        model = delivery
        fields = ['serial_no','delivery_number','delivery_date','truck_number','driver_name','recipient_name','delivery_comment']

class DeliverItemForm(forms.ModelForm):
    description = forms.ChoiceField(
    choices=[
        (item.item_name, item.item_name)  # Only include item_name without the model name prefix
        for item in sorted(
            chain(finished_goods.objects.all(), inventory.objects.all()),
            key=operator.attrgetter('item_name')
        )
    ],
    widget=forms.Select(attrs={
        'class': 'form-control select2',
        'data-minimum-input-length': '0',  # Start filtering from the first character
        'data-placeholder': 'Select or type an item',
        'id': 'description'
    }),
)

    
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
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'unit_type'}),
        
    )
    per_unit_kg = forms.FloatField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add value of KG per Unit', 'id': 'per_unit_kg'})
    )
        
    quantity = forms.IntegerField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantity',  'id':'quantity', 'readonly':'readonly'})
    )
    
    Measurement_unit_choices =( 
        ("", ""),
    ("kgs", "kgs"), 
    ("Pair", "Pair"),
    ("Pcs", "Pcs")) 

    measurement_unit = forms.ChoiceField(
        choices = Measurement_unit_choices,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'measurement_unit'}),
        
    )
    remark = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Remark', 'id':'remark'})
    )
    
    class Meta:
        model = delivery_items
        fields = ['description', 'no_of_unit', 'unit_type','per_unit_kg', 'quantity', 'measurement_unit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Refresh queryset to capture new items from finished_goods and inventory
        self.fields['description'].queryset = sorted(
            chain(finished_goods.objects.all(), inventory.objects.all()),
            key=operator.attrgetter('item_name')
        )


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
        
class CustomerForm(forms.ModelForm):
    
    contact_person = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Name'})
    )
    
    phone_number = forms.IntegerField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Company'})
    )
    
    email = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Email'})
    )
    
    company = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Company'})
    )

    address = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Address'})
    )
     
    class Meta:
        model = Customer
        fields = [ 'company','contact_person', 'phone_number', 'email','address']
