# Generated by Django 3.0.8 on 2020-08-02 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investigationOffice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sketch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.CharField(max_length=12)),
                ('sfile', models.FileField(upload_to='sketch')),
            ],
        ),
    ]
