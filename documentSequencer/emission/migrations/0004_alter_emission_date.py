# Generated by Django 5.0.6 on 2024-05-25 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emission', '0003_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emission',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
