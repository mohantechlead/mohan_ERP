from django import forms
#from .models import GRN, GRNItem
from .models import *

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

class GRNItemForm(forms.ModelForm):
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'quantity form-control' }))
    item_name = forms.ModelChoiceField(queryset=HS_code.objects.all(),
                                       empty_label="Item Name",
                                       widget=forms.Select(attrs={'class': 'item_name form-control'}),
                                       to_field_name='item_name')

    class Meta:
        
        model = GRN_item
        fields = ['item_name','quantity']

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

