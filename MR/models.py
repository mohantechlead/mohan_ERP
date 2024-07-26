from django.db import models
import uuid
# Create your models here.
class MR(models.Model):
    MR_no = models.TextField(primary_key= True)
    MR_date = models.DateField(blank= False)
    desc = models.TextField(blank=True)
    MR_store = models.TextField(blank=True)

class MR_item(models.Model):
    MR_no = models.ForeignKey('MR',on_delete= models.CASCADE,db_column = 'MR_no')
    quantity = models.FloatField(blank=True)
    item_name = models.TextField()
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    measurement_type = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null= True)
    description = models.TextField(blank=True, null= True)
    measurement_unit = models.TextField(blank=True, null= True)
    no_of_bags = models.FloatField(blank=True, null=True)
    per_unit_kg = models.FloatField(blank=True, null=True)

class inventory(models.Model):
    item_name = models.TextField(blank=True)
    no_of_unit = models.FloatField(blank=True, null=True)
    unit_type = models.TextField(blank=True, null=True)
    unit_measurment = models.TextField(blank=True, null=True)
    quantity = models.FloatField(blank=True)
    inventory_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.item_name

