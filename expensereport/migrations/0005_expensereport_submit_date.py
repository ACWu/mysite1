# Generated by Django 2.0.1 on 2018-01-22 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expensereport', '0004_expenseitem_telephone'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensereport',
            name='submit_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date submitted'),
        ),
    ]