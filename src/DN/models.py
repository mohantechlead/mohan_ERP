# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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
    delivery_date = models.DateField(blank=True)
    delivery_quantity = models.IntegerField(blank=True)
    truck_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    driver_name = models.TextField(blank=True, null=True)
    recipient_name = models.TextField(blank=True, null=True)
    delivery_comment = models.TextField(blank=True, null=True)

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
    description = models.TextField(blank=True, null=True)
    measurement = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)  # This field type is a guess.
    order_quantity = models.IntegerField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)
    remaining =  models.IntegerField(blank=True, null=True) # This field type is a guess.
    before_vat = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    withholding_amount = models.FloatField(blank=True, null=True)

    # class Meta:
    #     managed = False
    #     db_table = 'orders'



