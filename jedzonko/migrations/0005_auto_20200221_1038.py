# Generated by Django 2.2.6 on 2020-02-21 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0004_auto_20200221_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
