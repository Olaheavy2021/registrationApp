# Generated by Django 4.2.2 on 2023-07-09 10:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("studentregistration", "0004_rename_course_module_courses"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registration",
            name="registration_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
