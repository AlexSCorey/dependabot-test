# Generated by Django 3.2.12 on 2022-04-18 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0159_deprecate_inventory_source_UoPU_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='rrule',
            field=models.TextField(help_text='A value representing the schedules iCal recurrence rule.'),
        ),
    ]
