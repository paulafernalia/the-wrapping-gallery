# Generated by Django 5.0.7 on 2024-08-19 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wrappinggallery', '0023_alter_carry_mmposition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carry',
            name='mmposition',
            field=models.IntegerField(choices=[(-1, 'Follow tutorial'), (0, 'Centred'), (0.5, '0.5 DH off centre'), (1, '1 DH off centre'), (1.5, '1.5 DH off centre'), (2, '2 DH off centre'), (3, 'Centred on your chest'), (4, 'Centred on your back'), (5, 'Under your armpit')]),
        ),
    ]
