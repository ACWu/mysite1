# Generated by Django 2.0.1 on 2018-01-24 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expensereport', '0005_expensereport_submit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensereport',
            name='generate_date',
            field=models.DateTimeField(verbose_name='date created'),
        ),
    ]
