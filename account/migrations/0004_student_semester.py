# Generated by Django 4.0.3 on 2022-03-24 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_faculty_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='semester',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
