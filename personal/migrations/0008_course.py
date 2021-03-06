# Generated by Django 4.0.3 on 2022-03-20 01:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_faculty_username'),
        ('personal', '0007_alter_staffrecord_designation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=255)),
                ('course_code', models.CharField(max_length=255)),
                ('semester', models.CharField(choices=[('One', '1'), ('Two', '2'), ('Three', '3'), ('Four', '4'), ('Five', '5'), ('Six', '6'), ('Seven', '7'), ('Eight', '8')], max_length=50)),
                ('department', models.CharField(max_length=50)),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.faculty')),
            ],
        ),
    ]
