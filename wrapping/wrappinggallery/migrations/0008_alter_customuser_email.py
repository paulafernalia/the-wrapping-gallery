# Generated by Django 5.0.8 on 2024-10-03 15:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wrappinggallery", "0007_achievement_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="email address"
            ),
        ),
    ]
