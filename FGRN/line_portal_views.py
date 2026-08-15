from common.line_portals import make_portal_add_view, make_portal_list_view
from FGRN.line_portal_forms import InventoryFGRNItemsPortalForm
from FGRN.models import inventory_FGRN_items

_BASE = "fgrn_base.html"

manage_inventory_fgrn_items = make_portal_list_view(
    queryset_fn=lambda: inventory_FGRN_items.objects.all().order_by("item_name"),
    headers=["Item", "Total units", "Total qty", "Branch"],
    row_builder=lambda o: [
        o.item_name,
        o.total_no_of_unit,
        o.total_quantity,
        o.branch,
    ],
    title="Inventory FGRN items",
    add_url_name="manage_inventory_fgrn_items_add",
    base_template=_BASE,
)
manage_inventory_fgrn_items_add = make_portal_add_view(
    Form=InventoryFGRNItemsPortalForm,
    redirect_url_name="manage_inventory_fgrn_items",
    base_template=_BASE,
    title="Add inventory FGRN item",
)
