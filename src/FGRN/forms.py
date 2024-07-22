from django import forms
from .models import *


class FGRNForm(forms.ModelForm):

    STORE_CHOICES =( 
        ("", ""),
    ("STORE 1", "STORE 1"), 
    ("STORE 2", "STORE 2"),
    ("STORE 3 ", "STORE 3"),
    ("STORE 4 ", "STORE 4"),
    ("STORE 1 & 2 ", "STORE 1 & 2"),
    ("STORE 1 & 3 ", "STORE 1 & 3"),
    ("STORE 1 & 4 ", "STORE 1 & 4"),
    ("STORE 2 & 4 ", "STORE 2 & 4"),
    ("STORE 2 & 3 ", "STORE 2 & 3"),
    ("STORE 3 & 4 ", "STORE 3 & 4"),
    ("STORE 1, 2 & 3 ", "STORE 1, 2 & 3"),
    ("STORE 1, 2 & 4 ", "STORE 1, 2 & 4"),
    ("STORE 2, 3 & 4 ", "STORE 2, 3 & 4"),) 

    recieved_by = forms.ChoiceField(
        choices = STORE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),)
      
    class Meta:
        model = FGRN
        fields = ['FGRN_no','date','recieved_from','recieved_by', 'description']
   
class FGRNItemForm(forms.ModelForm):
    
    # item_name = forms.CharField(
    #     widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name', 'id': 'item_name','id': 'item_name',})
    # )
    item_name= forms.ModelChoiceField(
        queryset=finished_goods.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    description = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Description'})
    )
    no_of_unit = forms.CharField(
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
        model = FGRN_item
        fields = ['item_name','no_of_unit','unit_type','per_unit_kg','quantity','measurement_unit','remarks']
       