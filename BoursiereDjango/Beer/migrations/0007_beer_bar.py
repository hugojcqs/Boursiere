# Generated by Django 2.2.3 on 2019-07-05 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Beer', '0006_beer_alcohol_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='bar',
            field=models.IntegerField(default=1),
        ),
    ]