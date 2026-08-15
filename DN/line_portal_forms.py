"""ModelForms for DN inventory portals."""

from django import forms

from DN.models import inventory_order_items

_fc = {"class": "form-control"}


class InventoryOrderItemsPortalForm(forms.ModelForm):
    class Meta:
        model = inventory_order_items
        fields = ["item_name", "total_no_of_unit", "total_quantity", "branch", "group"]
        widgets = {
            "item_name": forms.TextInput(attrs=_fc),
            "total_no_of_unit": forms.TextInput(attrs=_fc),
            "total_quantity": forms.TextInput(attrs=_fc),
            "branch": forms.TextInput(attrs=_fc),
            "group": forms.TextInput(attrs=_fc),
        }
