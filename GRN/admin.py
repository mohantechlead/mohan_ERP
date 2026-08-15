from django.contrib import admin

from .models import (
    GRN,
    GRN_item,
    HS_code,
    ActualPurchase,
    ActualPurchaseItem,
    inventory_GRN_items,
    PR_item,
    purchase_orders,
    Supplier,
    VendorPayment,
)


@admin.register(purchase_orders)
class PurchaseOrdersAdmin(admin.ModelAdmin):
    search_fields = ("PR_no", "vendor_name", "site_name", "requested_by")


@admin.register(PR_item)
class PR_itemAdmin(admin.ModelAdmin):
    search_fields = ("item_name", "PR_no__PR_no")


class ActualPurchaseItemInline(admin.TabularInline):
    model = ActualPurchaseItem
    extra = 0


@admin.register(ActualPurchase)
class ActualPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "actual_purchase_id",
        "pr_no",
        "date",
        "created_by",
        "created_at",
    )
    list_filter = ("date", "created_at")
    search_fields = ("pr_no__PR_no", "created_by", "actual_purchase_id")
    readonly_fields = ("actual_purchase_id", "created_at")
    autocomplete_fields = ("pr_no",)
    inlines = (ActualPurchaseItemInline,)


@admin.register(ActualPurchaseItem)
class ActualPurchaseItemAdmin(admin.ModelAdmin):
    list_display = (
        "item_name",
        "actual_purchase",
        "pr_item",
        "requested_quantity",
        "actual_quantity",
        "difference_quantity",
    )
    list_filter = ("actual_purchase",)
    search_fields = ("item_name", "actual_purchase__pr_no__PR_no")
    autocomplete_fields = ("actual_purchase", "pr_item")


admin.site.register(GRN)
admin.site.register(GRN_item)
admin.site.register(HS_code)
admin.site.register(inventory_GRN_items)
admin.site.register(Supplier)
admin.site.register(VendorPayment)
