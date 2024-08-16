from django import forms
from .models import *

class MRForm(forms.ModelForm):
    
    
    class Meta:
   
        model = MR
        fields = ['MR_no','desc','date','MR_store']
   
class MRItemForm(forms.ModelForm):

    item_name= forms.ModelChoiceField(
        queryset=inventory.objects.all().order_by('item_name'),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
  
    no_of_unit = forms.FloatField(
        required = False,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add No of Units', 'id':'no_of_unit'})
    )

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
    per_unit_kg = forms.FloatField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add value of KG per Unit', 'id': 'per_unit_kg'})
    )
    quantity = forms.IntegerField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantity',  'id':'quantity'})
    )
    # measurement_unit = forms.CharField(
    #     widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add measurement units'})
    # )
    measurement_choice =( 
        ("", ""),
    ("kgs", "kgs")) 
    
    measurement_unit = forms.ChoiceField(
        choices = measurement_choice,
        widget=forms.Select(attrs={'class': 'form-control'}),
        
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
   
        model = opening_balance
        fields = ['item_name','quantity','no_of_unit','measurement_type','unit_type']
   
