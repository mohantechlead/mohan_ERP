from django import forms
from .models import *

class MRForm(forms.ModelForm):
    
    
    class Meta:
   
        model = MR
        fields = ['MR_no','desc','MR_date','MR_store']
   
class MRItemForm(forms.ModelForm):
    
    item_name = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'})
    )
    quantity = forms.IntegerField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'quantity'})
    )
    class Meta:
   
        model = MR_item
        fields = ['item_name','quantity']
   
class InventoryItemForm(forms.ModelForm):
    
    item_name = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'})
    )
    quantity = forms.IntegerField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'quantity'})
    )
    class Meta:
   
        model = inventory
        fields = ['item_name','quantity']
   