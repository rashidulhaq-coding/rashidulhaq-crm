# Generated by Django 3.1.5 on 2021-08-23 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='converted_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]