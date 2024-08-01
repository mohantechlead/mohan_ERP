from django import forms
#from .models import GRN, GRNItem
from .models import *
from MR.models import *

class PRForm(forms.ModelForm):
    PR_total_price = forms.DecimalField(
        decimal_places=2,
        required=False,
        widget=forms.TextInput(attrs={'class': 'total_price', 'readonly': 'readonly'})
    )

    PR_before_vat = forms.DecimalField(
        decimal_places=2,
        required=False,
        widget=forms.TextInput(attrs={'class': 'before_vat', 'readonly': 'readonly'})
    )
    class Meta:
        model = purchase_orders
        fields = ['PR_no','vendor_name','site_name','date','requested_by','approved_by', 'PR_before_vat', 'PR_total_price',"payment_type","measurement_type"]


class PRItemForm(forms.ModelForm):
    total_price = forms.DecimalField(
        decimal_places=2,
        required=False,
        widget=forms.TextInput(attrs={'class': 'total_price form-control', 'readonly': 'readonly'})
    )
    before_vat = forms.DecimalField(
        
        required=False,
        widget=forms.TextInput(attrs={'class': 'before_vat form-control', 'readonly': 'readonly'})
    )
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'quantity form-control' }))
    price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'price form-control'}))
    item_measurement = forms.CharField(widget=forms.TextInput(attrs={'class': 'item_measurement form-control'}), required=False)
    item_name = forms.ModelChoiceField(queryset=HS_code.objects.all(),
                                       empty_label="Item Name",
                                       widget=forms.Select(attrs={'class': 'item_name form-control'}),
                                       to_field_name='item_name')
    hs_code = forms.CharField(label='HS CODE', required=False, widget=forms.TextInput(attrs={'class': 'hs_codes form-control'}))
    
    class Meta:
   
        model = PR_item
        fields = ['item_name','hs_code','price','quantity','before_vat','total_price','item_measurement']

        def clean(self):
            cleaned_data = super().clean()
            
            for field_name in ['quantity', 'before_vat']:
                quantity = cleaned_data.get(f'{quantity}_0')
                before_vat = cleaned_data.get(f'{before_vat}_1')

                if quantity is not None and before_vat is not None:
                    total_price = quantity * before_vat
                    cleaned_data[f'total_price_{total_price}'] = total_price
                    print("not")

            return cleaned_data



class GRNForm(forms.ModelForm):
    class Meta:
        model = GRN
        fields = ['GRN_no','grn_date','recieved_from','store_name','store_keeper','status','transporter_name','truck_no']

class ImportGRNForm(forms.ModelForm):
    class Meta:
        model = import_GRN
        fields = ['GRN_no','grn_date','recieved_from','store_name','store_keeper','transporter_name','truck_no']

class ImportGRNItemForm(forms.ModelForm):
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


class GRNItemForm(forms.ModelForm):
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

class approvalForm(forms.Form):
    selected_orders = forms.ModelMultipleChoiceField(
        queryset= purchase_orders.objects.filter(status='Pending'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    action = forms.ChoiceField(
        choices=[('approve', 'Approve'), ('reject', 'Reject')],
        widget=forms.RadioSelect,
    )
    approval = forms.CharField(
        widget=forms.TextInput,
        required=False  # You can omit this line as TextInput is the default widget for CharField
    )

