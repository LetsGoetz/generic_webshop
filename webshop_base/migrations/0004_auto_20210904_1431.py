# Generated by Django 3.2.6 on 2021-09-04 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop_base', '0003_auto_20210904_1055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productitem',
            old_name='measurementUnit',
            new_name='measurement_unit_name_plural',
        ),
        migrations.RenameField(
            model_name='productitem',
            old_name='quantityInStock',
            new_name='quantity_in_stock',
        ),
        migrations.RenameField(
            model_name='productitem',
            old_name='sellingUnit',
            new_name='selling_unit',
        ),
        migrations.AddField(
            model_name='productitem',
            name='measurement_unit_name_single',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='quantity_of_SU',
            field=models.IntegerField(null=True),
        ),
    ]
