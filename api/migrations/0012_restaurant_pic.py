# Generated by Django 4.0.4 on 2022-05-01 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_meal_num_of_diners_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='pic',
            field=models.URLField(default='https://images.app.goo.gl/RDQtoViqEvvGQc587'),
        ),
    ]
