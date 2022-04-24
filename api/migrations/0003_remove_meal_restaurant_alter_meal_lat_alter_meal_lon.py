# Generated by Django 4.0.4 on 2022-04-24 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_meal_user_friends_restaurant_meal_creator_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='restaurant',
        ),
        migrations.AlterField(
            model_name='meal',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='meal',
            name='lon',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
