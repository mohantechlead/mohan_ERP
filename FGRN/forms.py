from django import forms
from .models import *


class FinishedGoodsGroupForm(forms.ModelForm):
    class Meta:
        model = FinishedGoodsGroup
        fields = ['finished_good', 'order_items']
        widgets = {
            'order_items': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        finished_good = kwargs.get('instance', None)
        
        # If the form is being initialized with data (POST request), try to capture finished_good
        if 'data' in kwargs:
            data = kwargs['data']
            finished_good_id = data.get('finished_good', None)
            if finished_good_id:
                finished_good = finished_good_id
        
        # Check if finished_good is provided and filter the order_items
        if finished_good:
            # Find all existing FinishedGoodsGroup entries with the given finished_good
            existing_order_items = FinishedGoodsGroup.objects.filter(finished_good=finished_good)
            
            # Collect all order_items that are already assigned to this finished_good
            existing_items = [item for group in existing_order_items for item in group.order_items.all()]
            queryset = inventory_order_items.objects.exclude(id__in=[item.id for item in existing_items])
        else:
            queryset = inventory_order_items.objects.all()

        super().__init__(*args, **kwargs)
        
        # Apply the filtered queryset to the order_items field
        self.fields['order_items'].queryset = queryset


class FGRNForm(forms.ModelForm):
    FGRN_no = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'FGRN Number', 'id': 'FGRN_no'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'date'})
    )
    recieved_from = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Received From', 'id': 'recieved_from', 'list': 'received_options'})
    )
    recieved_by = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Received By', 'id': 'recieved_by', 'list':'recieved_by_option'})
    )
    
    class Meta:
        model = FGRN
        fields = ['FGRN_no', 'date', 'recieved_from', 'recieved_by', 'branch']
   
class FGRNItemForm(forms.ModelForm):
    
    item_name= forms.ModelChoiceField(
        queryset=items_list.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id':'item_name'}),
    )
    description = forms.ModelChoiceField(
        queryset=finished_goods.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id':'description'}),)
    
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

       