# Generated by Django 4.0.3 on 2022-03-16 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0003_alter_staffrecord_designation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=50)),
            ],
        ),
    ]
