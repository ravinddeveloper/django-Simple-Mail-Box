# Generated by Django 4.2.4 on 2023-11-04 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailapp', '0006_user_verify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_verify',
            name='user',
            field=models.CharField(default='none', max_length=500),
        ),
    ]
