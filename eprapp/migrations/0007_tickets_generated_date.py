# Generated by Django 5.0.4 on 2024-04-28 11:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eprapp', '0006_rename_num_tickets_genrated_tickets_num_tickets_generated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='generated_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
