from django import forms
from .models import *
from DN.models import inventory_order_items
from itertools import chain
from FGRN.models import finished_goods
import operator

class FGRNForm(forms.ModelForm):
    FGRN_no = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'FGRN Number', 'id': 'FGRN_no'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'date'})
    )
    recieved_from = forms.CharField(
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Received From',
            'id': 'recieved_from',
            'list': 'received_options',
            'autocomplete': 'off'  # Disable autocomplete
        }
    )
)
    recieved_by = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 
                                      'placeholder': 'Received By', 
                                      'id': 'recieved_by',
                                       'list':'recieved_by_option', 
                                       'autocomplete': 'off'})
    )
    
    class Meta:
        model = FGRN
        fields = ['FGRN_no', 'date', 'recieved_from', 'recieved_by', 'branch']
   
class FGRNItemForm(forms.ModelForm):
    
    item_name= forms.ModelChoiceField(
        queryset=items_list.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id':'item_name'}),
    )

    # Collect both querysets and ensure uniqueness of item_name values
    inventory_items = list(chain(inventory_order_items.objects.all(), inventory_FGRN_items.objects.all()))

   
    # Create a set to track unique item names
    seen_item_names = set()
    unique_items = []

    # Loop through the combined querysets and ensure uniqueness
    for item in inventory_items:
        if item.item_name not in seen_item_names:
            seen_item_names.add(item.item_name)
            unique_items.append(item)

    # Now sort the unique items by item_name
    sorted_unique_items = sorted(unique_items, key=operator.attrgetter('item_name'))

    # Create the ChoiceField with sorted and unique items
    description = forms.ChoiceField(
        choices=[
            (item.item_name, item.item_name)  # Only include item_name for value and label
            for item in sorted_unique_items
        ],
        widget=forms.Select(attrs={
            'class': 'form-control select2',  # Class for Select2 widget styling
            'data-minimum-input-length': '0',  # Start filtering from the first character
            'data-placeholder': 'Select or type an item',  # Placeholder text
            'id': 'description',  # HTML ID for the field
        }),
    )
    
    # description = forms.ModelChoiceField(
    #     queryset=finished_goods.objects.all(),
    #     widget=forms.Select(attrs={'class': 'form-control', 'id':'description'}),)
    
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
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantity',  'id':'quantity'})
    )

    Measurement_unit_choices =( 
        ("", ""),
    ("kgs", "kgs")) 

    # measurement_unit = forms.CharField(
    #     widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add measurement units'})
    # )
    measurement_unit = forms.ChoiceField(
        choices = Measurement_unit_choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        
    )
   
    class Meta:
        model = FGRN_item
        fields = ['description','item_name','no_of_unit','unit_type','per_unit_kg','quantity','measurement_unit']

class OpeningBalanceItemForm(forms.ModelForm):

    UNIT_CHOICES =( 
        ("", ""),
    ("Bag", "Bag"), 
    ("Pkg", "Pkg"),
    ("Crt", "Crt"),
    ("Drum", "Drum"),) 
    
    unit_type = forms.ChoiceField(
        choices = UNIT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        
    )

    measurement_choice =( 
        ("", ""),
    ("kgs", "kgs")) 
    
    measurement_type = forms.ChoiceField(
        choices = measurement_choice,
        widget=forms.Select(attrs={'class': 'form-control'}),
        
    )
    
    class Meta:
   
        model = FGRNopening_balance
        fields = ['item_name','quantity','no_of_unit','measurement_type','unit_type']
    
class InventoryItemForm(forms.ModelForm):
    
    class Meta:
   
        model = finished_goods
        fields = ['item_name','quantity','no_of_unit','measurement_type','unit_type']

       
