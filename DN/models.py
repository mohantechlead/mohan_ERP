from django.db import models
import uuid

class trial_delivery(models.Model):
    name = models.IntegerField(primary_key=True)
    serial_no = models.ForeignKey('Orders', models.DO_NOTHING, db_column='serial_no')
    delivery_date = models.DateField(blank=True)
    delivery_quantity = models.IntegerField(blank=True)
    truck_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    driver_name = models.TextField(blank=True, null=True)
    recipient_name = models.TextField(blank=True, null=True)
    delivery_comment = models.TextField(blank=True, null=True)

    
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

    def __str__(self):
        return self.serial_no

    class Meta:
        db_table = 'order'

class orders_items(models.Model):
    serial_no = models.ForeignKey('orders', on_delete=models.CASCADE,db_column = 'serial_no', related_name="orders")
    description = models.TextField(blank=True, null=True)
    no_of_unit = models.FloatField(blank=True, null=True)
    unit_type = models.TextField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    per_unit_kg = models.FloatField(blank=True, null=True)
    unit_price = models.FloatField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)  
    remaining_quantity =  models.FloatField(blank=True, null=True) 
    remaining_unit = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{str(self.serial_no)} - {self.description}'
    
class delivery(models.Model):
    delivery_number = models.IntegerField(primary_key=True)
    # serial_no = models.ForeignKey('orders', models.DO_NOTHING, db_column='serial_no', related_name='deliveries')
    serial_no = models.ForeignKey('orders', on_delete=models.CASCADE, related_name='deliveries')  # This allows multiple deliveries for the same order
    delivery_date = models.DateField(blank=True)
    # delivery_quantity = models.IntegerField(blank=True)
    truck_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    driver_name = models.TextField(blank=True, null=True)
    recipient_name = models.TextField(blank=True, null=True)
    delivery_comment = models.TextField(blank=True, null=True)
    total_quantity = models.FloatField(blank=True, null=True)
    total_bags = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.delivery_number)
    
class delivery_items(models.Model):
    # serial_no = models.ForeignKey('delivery', on_delete=models.CASCADE,db_column = 'serial_no', related_name='orders')
    delivery_number = models.ForeignKey('delivery', on_delete=models.CASCADE,db_column = 'delivery_number', related_name='delivery')
    description = models.TextField(blank=True, null=True)
    no_of_unit = models.FloatField(blank=True, null=True)
    unit_type = models.TextField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    per_unit_kg = models.FloatField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{str(self.delivery_number)} - {self.description}'

class Customer(models.Model):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name



