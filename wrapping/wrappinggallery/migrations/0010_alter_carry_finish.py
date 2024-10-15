# Generated by Django 5.0.9 on 2024-10-15 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wrappinggallery', '0009_carry_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carry',
            name='finish',
            field=models.CharField(choices=[('knotless', 'Knotless'), ('knotless tibetan', 'Knotless Tibetan'), ('tibetan', 'Tibetan'), ('TUB', 'Tied under bum'), ('TIF', 'Tied in front'), ('TAS', 'Tied at shoulder'), ('buleria', 'Buleria'), ('CCCB', 'Candy Cane Chest Belt'), ('slipknot', 'Slipknot'), ('ring(s)', 'Rings'), ('rapunzel', 'Rapunzel'), ('tied at the back', 'Tied at the back'), ('other double knot', 'Double Knot (other)'), ('strangleproof', 'Strangleproof')], max_length=20),
        ),
    ]
