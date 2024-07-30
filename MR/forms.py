from django import forms
from .models import *

class MRForm(forms.ModelForm):
    
    
    class Meta:
   
        model = MR
        fields = ['MR_no','desc','MR_date','MR_store']
   
class MRItemForm(forms.ModelForm):

    item_name= forms.ModelChoiceField(
        queryset=inventory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    description = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Description'})
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
        widget=forms.Select(attrs={'class': 'form-control'}),
        
    )
    per_unit_kg = forms.FloatField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add value of KG per Unit', 'id': 'per_unit_kg'})
    )
    quantity = forms.IntegerField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantity',  'id':'quantity'})
    )
    measurement_unit = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add measurement units'})
    )
    remarks = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Remark'})
    )
    class Meta:
        model = MR_item
        fields = ['item_name','no_of_unit','unit_type','per_unit_kg','quantity','measurement_unit','remarks']
   
class InventoryItemForm(forms.ModelForm):
    
    class Meta:
   
        model = inventory
        fields = ['item_name','quantity','no_of_unit','measurement_type','unit_type']
   