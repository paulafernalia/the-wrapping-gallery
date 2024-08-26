# Generated by Django 5.0.8 on 2024-08-23 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wrappinggallery', '0027_carry_longtitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='carry',
            name='pass_cross',
            field=models.IntegerField(choices=[(0, ''), (1, ''), (2, '(2)'), (3, '(3)')], default=0),
        ),
        migrations.AddField(
            model_name='carry',
            name='pass_horizontal',
            field=models.IntegerField(choices=[(0, ''), (1, ''), (2, '(2)'), (3, '(3)')], default=0),
        ),
        migrations.AddField(
            model_name='carry',
            name='pass_kangaroo',
            field=models.IntegerField(choices=[(0, ''), (1, ''), (2, '(2)'), (3, '(3)')], default=0),
        ),
        migrations.AddField(
            model_name='carry',
            name='pass_poppins',
            field=models.IntegerField(choices=[(0, ''), (1, ''), (2, '(2)'), (3, '(3)')], default=0),
        ),
        migrations.AddField(
            model_name='carry',
            name='pass_reinforcing_cross',
            field=models.IntegerField(choices=[(0, ''), (1, ''), (2, '(2)'), (3, '(3)')], default=0),
        ),
        migrations.AddField(
            model_name='carry',
            name='pass_reinforcing_horizontal',
            field=models.IntegerField(choices=[(0, ''), (1, ''), (2, '(2)'), (3, '(3)')], default=0),
        ),
        migrations.AddField(
            model_name='carry',
            name='pass_ruck',
            field=models.IntegerField(choices=[(0, ''), (1, ''), (2, '(2)'), (3, '(3)')], default=0),
        ),
        migrations.AddField(
            model_name='carry',
            name='pass_sling',
            field=models.IntegerField(choices=[(0, ''), (1, ''), (2, '(2)'), (3, '(3)')], default=0),
        ),
    ]
