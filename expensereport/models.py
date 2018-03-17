import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class ExpenseReport(models.Model):
    generate_date = models.DateTimeField('date created')
    submit_date = models.DateTimeField('date submitted', null=True, blank=True)
    title = models.CharField(max_length=200)
    ending_mileage = models.IntegerField()
    added_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.generate_date.strftime('%m/%d/%Y')
        
    def was_generated_recently(self):
        return self.generate_date >= timezone.now() - datetime.timedelta(days=7)

    was_generated_recently.admin_order_field = 'generate_date'
    was_generated_recently.boolean = True
    was_generated_recently.short_description = 'Generated recently?'
    
class ExpenseItem(models.Model):
    expense_report = models.ForeignKey(ExpenseReport, on_delete=models.CASCADE)
    item_date = models.DateField()
    meals = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    hotel = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    telephone = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    transportation = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    misc = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    description = models.CharField(max_length=500)
    
    def __str__(self):
        return self.item_date.strftime('%m/%d/%Y')
