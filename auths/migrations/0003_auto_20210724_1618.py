# Generated by Django 3.2.5 on 2021-07-24 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_role',
            field=models.CharField(default='customer', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]