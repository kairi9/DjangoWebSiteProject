# Generated by Django 3.1.6 on 2021-04-18 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lineapp', '0002_auto_20210418_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineaccount',
            name='line_id',
            field=models.CharField(editable=False, max_length=150, unique=True),
        ),
    ]
