# Generated by Django 3.2.25 on 2024-06-02 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo_crud', '0012_rename_estareporte_customjobmanagement_reporte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customworkmanagement',
            name='reporte',
            field=models.CharField(max_length=1500, verbose_name='Reporte'),
        ),
    ]
