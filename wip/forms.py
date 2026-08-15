from django import forms

from MR.models import inventory

from .models import WIP, WIP_item


class WIPForm(forms.ModelForm):
    WIP_no = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'WIP Number',
                'id': 'WIP_no',
            }
        )
    )
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date', 'id': 'date'}
        )
    )
    work_center = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Work center / department',
                'id': 'work_center',
            }
        ),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Notes',
                'id': 'notes',
            }
        ),
    )
    branch = forms.IntegerField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'branch'},
            choices=[('', ''), (1, '1'), (2, '2')],
        ),
    )

    class Meta:
        model = WIP
        fields = ['WIP_no', 'date', 'work_center', 'notes', 'branch']


class WIPItemForm(forms.ModelForm):
    inventory_pick = forms.ModelChoiceField(
        label='Item name',
        queryset=inventory.objects.all().order_by('item_name'),
        required=False,
        empty_label='---------',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    no_of_unit = forms.FloatField(
        required=False,
        label='No of unit',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Add No of Units',
                'id': 'no_of_unit',
            }
        ),
    )
    UNIT_CHOICES = (
        ('', ''),
        ('Bag', 'Bag'),
        ('Pkg', 'Pkg'),
        ('Crt', 'Crt'),
        ('Drum', 'Drum'),
    )
    unit_type = forms.ChoiceField(
        label='Unit type',
        choices=UNIT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    per_unit_kg = forms.FloatField(
        required=False,
        label='Per unit kg',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Add value of KG per Unit',
                'id': 'per_unit_kg',
            }
        ),
    )
    quantity = forms.FloatField(
        required=False,
        label='Quantity',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'id': 'quantity',
            }
        ),
    )
    MEASUREMENT_CHOICES = (
        ('', ''),
        ('kgs', 'kgs'),
    )
    measurement_type = forms.ChoiceField(
        label='Measurement unit',
        choices=MEASUREMENT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    remarks = forms.CharField(
        required=False,
        label='Remarks',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Add Remark',
            }
        ),
    )

    class Meta:
        model = WIP_item
        fields = [
            'quantity',
            'no_of_unit',
            'unit_type',
            'per_unit_kg',
            'measurement_type',
            'remarks',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_fields(
            [
                'inventory_pick',
                'no_of_unit',
                'unit_type',
                'per_unit_kg',
                'quantity',
                'measurement_type',
                'remarks',
            ]
        )
