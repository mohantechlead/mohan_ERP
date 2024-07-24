from django.db import models

# Create your models here.
class FGRN(models.Model):
    FGRN_no = models.TextField(primary_key= True)
    recieved_from = models.TextField(blank=True, null= True)
    recieved_by = models.TextField(blank=True, null= True)
    description = models.TextField(blank=True, null= True)
    date = models.DateField()
    total_quantity = models.FloatField(blank=True, null=True)

class FGRN_item(models.Model):
    FGRN_no = models.ForeignKey('FGRN', on_delete=models.CASCADE,db_column = 'FGRN_no')
    item_id = models.AutoField(primary_key= True)
    item_name = models.TextField(blank=True, null= True)
    quantity = models.FloatField()
    remarks = models.TextField(blank=True, null= True)
    description = models.TextField(blank=True, null= True)
    measurement_unit = models.TextField(blank=True, null= True)
    no_of_bags = models.FloatField(blank=True, null=True)

class finished_goods(models.Model):
    item_name = models.TextField(primary_key=True)
    quantity = quantity = models.FloatField()

    def __str__(self):
        return self.item_name
    
class items_list(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.item_name