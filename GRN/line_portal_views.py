from common.line_portals import make_portal_add_view, make_portal_list_view
from GRN.line_portal_forms import InventoryGRNItemsPortalForm
from GRN.models import inventory_GRN_items

_BASE = "grn_base.html"

manage_inventory_grn_items = make_portal_list_view(
    queryset_fn=lambda: inventory_GRN_items.objects.all().order_by("item_name"),
    headers=["Item", "Total units", "Total qty", "Branch"],
    row_builder=lambda o: [
        o.item_name,
        o.total_no_of_unit,
        o.total_quantity,
        o.branch,
    ],
    title="Inventory GRN items",
    add_url_name="manage_inventory_grn_items_add",
    base_template=_BASE,
)
manage_inventory_grn_items_add = make_portal_add_view(
    Form=InventoryGRNItemsPortalForm,
    redirect_url_name="manage_inventory_grn_items",
    base_template=_BASE,
    title="Add inventory GRN item",
)
