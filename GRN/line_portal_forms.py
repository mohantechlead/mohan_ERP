"""ModelForms for GRN add-only portal (inventory_GRN_items)."""

from django import forms

from GRN.models import inventory_GRN_items

_fc = {"class": "form-control"}


class InventoryGRNItemsPortalForm(forms.ModelForm):
    class Meta:
        model = inventory_GRN_items
        fields = ["item_name", "total_no_of_unit", "total_quantity", "branch"]
        widgets = {
            "item_name": forms.TextInput(attrs=_fc),
            "total_no_of_unit": forms.TextInput(attrs=_fc),
            "total_quantity": forms.TextInput(attrs=_fc),
            "branch": forms.TextInput(attrs=_fc),
        }
