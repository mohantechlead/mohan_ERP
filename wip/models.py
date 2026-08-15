from django.db import models


class WIP(models.Model):
    WIP_no = models.TextField(primary_key=True)
    date = models.DateField()
    work_center = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    branch = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['WIP_no']

    def __str__(self):
        return str(self.WIP_no)


class WIP_item(models.Model):
    WIP_no = models.ForeignKey(
        WIP,
        on_delete=models.CASCADE,
        db_column='WIP_no',
        related_name='wip_items',
    )
    item_id = models.AutoField(primary_key=True)
    item_name = models.TextField()
    quantity = models.FloatField(blank=True, null=True)
    no_of_unit = models.FloatField(blank=True, null=True)
    unit_type = models.TextField(blank=True, null=True)
    per_unit_kg = models.FloatField(blank=True, null=True)
    measurement_type = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['WIP_no', 'item_id']

    def __str__(self):
        return f'{self.WIP_no} — {self.item_name}'
