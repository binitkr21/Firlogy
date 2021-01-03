# Generated by Django 3.0.8 on 2020-07-25 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('aadhaar_number', models.CharField(max_length=12)),
                ('city', models.CharField(max_length=45)),
                ('state', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=15)),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True)),
                ('number_of_cases', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
    ]