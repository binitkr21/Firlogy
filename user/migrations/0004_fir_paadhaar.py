# Generated by Django 3.0.8 on 2020-07-31 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200731_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='fir',
            name='paadhaar',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
