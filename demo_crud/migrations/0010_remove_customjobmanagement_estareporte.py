# Generated by Django 3.2.25 on 2024-06-02 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo_crud', '0009_alter_customjobmanagement_estareporte'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customjobmanagement',
            name='estareporte',
        ),
    ]
