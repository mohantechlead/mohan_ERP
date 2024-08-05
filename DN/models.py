from django.db import models

class trial_delivery(models.Model):
    name = models.IntegerField(primary_key=True)
    serial_no = models.ForeignKey('Orders', models.DO_NOTHING, db_column='serial_no')
    delivery_date = models.DateField(blank=True)
    delivery_quantity = models.IntegerField(blank=True)
    truck_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    driver_name = models.TextField(blank=True, null=True)
    recipient_name = models.TextField(blank=True, null=True)
    delivery_comment = models.TextField(blank=True, null=True)

    # class Meta:
    #     managed = False
    #     db_table = 'trial_delivery'

class delivery(models.Model):
    delivery_number = models.IntegerField(primary_key=True)
    serial_no = models.ForeignKey('Orders', models.DO_NOTHING, db_column='serial_no')
    # description = models.TextField('Orders', models.DO_NOTHING, db_column='description')
    delivery_date = models.DateField(blank=True)
    delivery_quantity = models.IntegerField(blank=True)
    truck_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    driver_name = models.TextField(blank=True, null=True)
    recipient_name = models.TextField(blank=True, null=True)
    delivery_comment = models.TextField(blank=True, null=True)

# class delivery(models.Model):
#     delivery_number = models.IntegerField(primary_key=True)
#     serial_no = models.ForeignKey('Orders', models.DO_NOTHING, db_column='serial_no')
#     # description = models.TextField('Orders', models.DO_NOTHING, db_column='description')
#     delivery_date = models.DateField(blank=True)
#     delivery_quantity = models.IntegerField(blank=True)
#     truck_number = models.TextField(blank=True, null=True)  # This field type is a guess.
#     driver_name = models.TextField(blank=True, null=True)
#     recipient_name = models.TextField(blank=True, null=True)
#     delivery_comment = models.TextField(blank=True, null=True)

    # class Meta:
    #     managed = False
    #     db_table = 'delivery'


class orders(models.Model):
    customer_name = models.TextField()
    tin_no = models.TextField()
    serial_no = models.TextField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    invoice = models.TextField(unique=True, blank=True, null=True)
    invoice_type = models.TextField(blank=True, null=True)
    total_bags = models.TextField(blank=True, null=True)
    final_price = models.FloatField(blank=True, null=True)
    before_vat = models.FloatField(blank=True, null=True)
    withholding_amount = models.FloatField(blank=True, null=True)
    vat_amount = models.FloatField(blank=True, null=True)
    reciveable = models.FloatField(blank=True, null=True)

    # measurement = models.TextField(blank=True, null=True)
    # price = models.FloatField(blank=True, null=True)  # This field type is a guess.
    # order_quantity = models.IntegerField(blank=True, null=True)
    # total_price = models.FloatField(blank=True, null=True)
    # remaining =  models.IntegerField(blank=True, null=True) # This field type is a guess.
    # before_vat = models.FloatField(blank=True, null=True)
    # comment = models.TextField(blank=True, null=True)
    # withholding_amount = models.FloatField(blank=True, null=True)

class orders_items(models.Model):
    serial_no = models.ForeignKey('orders', on_delete=models.CASCADE,db_column = 'serial_no')
    description = models.TextField(blank=True, null=True)
    no_of_unit = models.FloatField(blank=True, null=True)
    unit_type = models.TextField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    per_unit_kg = models.FloatField(blank=True, null=True)
    unit_price = models.FloatField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)  
    # order_quantity = models.FloatField(blank=True, null=True)
    remaining_quantity =  models.FloatField(blank=True, null=True) 
    remaining_unit = models.FloatField(blank=True, null=True)
    

    # class Meta:
    #     managed = False
    #     db_table = 'orders'



