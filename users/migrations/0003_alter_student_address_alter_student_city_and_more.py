# Generated by Django 4.2.2 on 2023-07-04 12:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_student_options_alter_student_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="address",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="city",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="country",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="dob",
            field=models.DateField(blank=True, null=True),
        ),
    ]
