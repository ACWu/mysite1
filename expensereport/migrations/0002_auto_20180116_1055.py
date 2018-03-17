# Generated by Django 2.0.1 on 2018-01-16 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expensereport', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenseitem',
            name='hotel',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='expenseitem',
            name='misc',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='expenseitem',
            name='transportation',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='expenseitem',
            name='meals',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]