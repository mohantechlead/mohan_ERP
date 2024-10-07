from django.db import models
import uuid
# Create your models here.
class purchase_orders(models.Model):
    vendor_name = models.TextField(blank=True, null=True)
    PR_no = models.TextField(primary_key=True, db_column='pr_no')
    date = models.DateField(blank=True, null=True)
    site_name = models.TextField( )
    payment_type = models.TextField(blank=True, null=True)
    requested_by = models.TextField(blank=True, null=True)
    approved_by = models.TextField(blank=True, null=True)
    PR_total_price = models.FloatField(blank=True, null=True, db_column='pr_total_price')
    PR_before_vat = models.FloatField(blank=True, null=True, db_column="pr_before_vat")
    status = models.TextField(blank=True, null=True, default="Pending")
    total_quantity = models.FloatField(blank=True, null=True)
    measurement_type = models.TextField(blank=True, null=True)
    remaining = models.FloatField(blank=True, null=True)
    vat = models.FloatField(blank=True, null=True)
    excise_tax = models.FloatField(blank=True, null=True)

class PR_item(models.Model):
    PR_no = models.ForeignKey('purchase_orders', on_delete=models.CASCADE, db_column='PR_no',blank=True, null=True)
    id_numeric = models.AutoField(primary_key=True)
    item_name = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    before_vat = models.FloatField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)
    quantity = models.FloatField()
    remaining = models.FloatField()
    item_measurement = models.TextField(blank=True, null=True)
    
class GRN(models.Model):
    GRN_no = models.TextField(primary_key=True)
    PR_no = models.ForeignKey('purchase_orders', on_delete=models.CASCADE, db_column='PR_no', null=True, blank=True)
    date = models.DateField(blank=True, null=True)
    recieved_from = models.TextField(blank=True, null=True)
    transporter_name = models.TextField(blank=True, null=True)
    truck_no = models.TextField(blank=True, null=True)
    store_name =  models.TextField(blank=True, null=True) # This field type is a guess.
    store_keeper = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['GRN_no'] 

    def __str__(self):
        return str(self.GRN_no)
    
class GRN_item(models.Model):
    # PR_no = models.ForeignKey('purchase_orders', on_delete=models.CASCADE, db_column='PR_no')
    GRN_no = models.ForeignKey('GRN', on_delete=models.CASCADE, db_column='GRN_no')
    grn_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    measurement_type = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null= True)
    description = models.TextField(blank=True, null= True)
    measurement_unit = models.TextField(blank=True, null= True)
    no_of_unit = models.FloatField(blank=True, null=True)
    per_unit_kg = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['GRN_no'] 

    def __str__(self):
        return f'{self.GRN_no} - {self.item_name}'

class import_GRN(models.Model):
    GRN_no = models.TextField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    recieved_from = models.TextField(blank=True, null=True)
    transporter_name = models.TextField(blank=True, null=True)
    truck_no = models.TextField(blank=True, null=True)
    store_name =  models.TextField(blank=True, null=True) # This field type is a guess.
    store_keeper = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['GRN_no'] 

class import_GRN_item(models.Model):
    GRN_no = models.ForeignKey('import_GRN', on_delete=models.CASCADE, db_column='GRN_no')
    grn_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.TextField(blank=True, null=True)
    quantity = models.FloatField()
    measurement_type = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null= True)
    description = models.TextField(blank=True, null= True)
    measurement_unit = models.TextField(blank=True, null= True)
    no_of_unit = models.FloatField(blank=True, null=True)
    per_unit_kg = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['GRN_no'] 

    def __str__(self):
        return f'{self.GRN_no} - {self.item_name}'
    
class HS_code(models.Model):
    number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hs_code = models.TextField(blank=True, null=True)
    item_name = models.TextField(blank=False, null=False)

    class Meta:
        ordering = ['item_name']

    def __str__(self):
     return self.item_name
    
class inventory_GRN_items(models.Model):
    item_name = models.TextField(blank=True)
    total_no_of_unit = models.FloatField(blank=True, null=True)
    total_quantity = models.FloatField(blank=True)
    inventory_GRN_items_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['item_name']

    def __str__(self):
     return self.item_name
    
class Supplier(models.Model):
    supplier_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact_person = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    


    