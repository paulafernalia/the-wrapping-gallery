# Generated by Django 5.0.7 on 2024-08-01 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wrappinggallery', '0017_alter_carry_shoulders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carry',
            name='shoulders',
            field=models.IntegerField(choices=[(0, 'Zero (torso carry)'), (1, 'One'), (2, 'Two')]),
        ),
    ]
