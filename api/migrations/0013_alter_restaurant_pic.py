# Generated by Django 4.0.4 on 2022-05-01 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_restaurant_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='pic',
            field=models.URLField(blank=True),
        ),
    ]
