from django.db import models
import uuid

# Create your models here.
class FGRN(models.Model):
    FGRN_no = models.TextField(primary_key= True)
    recieved_from = models.TextField(blank=True, null= True)
    recieved_by = models.TextField(blank=True, null= True)
    description = models.TextField(blank=True, null= True)
    date = models.DateField()
    total_quantity = models.FloatField(blank=True, null=True)
    total_bags = models.FloatField(blank=True, null=True)
    total_crt = models.FloatField(blank=True, null=True)
    total_Pkg = models.FloatField(blank=True, null=True)
    branch = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.FGRN_no)
    
    class Meta:
        ordering = ['FGRN_no'] 

class FGRN_item(models.Model):
    FGRN_no = models.ForeignKey('FGRN', on_delete=models.CASCADE,db_column = 'FGRN_no')
    item_id = models.AutoField(primary_key= True)
    item_name = models.TextField(blank=True, null= True, default="-")
    quantity = models.FloatField()
    remarks = models.TextField(blank=True, null= True)
    description = models.TextField(blank=True, null= True)
    measurement_unit = models.TextField(blank=True, null= True)
    no_of_unit = models.FloatField(blank=True, null=True)
    per_unit_kg = models.FloatField(blank=True, null=True)
    unit_type = models.TextField(blank=True, null= True)

    def __str__(self):
      return f'{str(self.FGRN_no)} - {self.description}'
 
    class Meta:
        ordering = ['FGRN_no'] 

        


class finished_goods(models.Model):
    item_name = models.TextField(primary_key=True)
    quantity = quantity = models.FloatField(blank=True, null=True)
    no_of_unit = models.FloatField(blank=True, null=True, default=0)
    unit_type = models.TextField(blank=True, null=True)
    measurement_type = models.TextField(blank=True, null=True)
   
    
    def __str__(self):
        return self.item_name
    
    class Meta:
        ordering = ['item_name'] 

    
class items_list(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.item_name
    
class FGRNopening_balance(models.Model):
    item_name = models.TextField(blank=True)
    no_of_unit = models.FloatField(blank=True, null=True)
    unit_type = models.TextField(blank=True, null=True)
    measurement_type = models.TextField(blank=True, null=True)
    quantity = models.FloatField(blank=True)
    balance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['item_name'] 

    def __str__(self):
        return self.item_name
    
class inventory_FGRN_items(models.Model):
    item_name = models.TextField(blank=True)
    total_no_of_unit = models.FloatField(blank=True, null=True)
    total_quantity = models.FloatField(blank=True)
    balance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['item_name'] 

    def __str__(self):
        return self.item_name

