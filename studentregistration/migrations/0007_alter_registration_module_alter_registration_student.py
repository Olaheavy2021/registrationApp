# Generated by Django 4.2.2 on 2023-07-12 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_student_address_alter_student_city_and_more"),
        ("studentregistration", "0006_merge_20230710_1522"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registration",
            name="module",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="registrations",
                to="studentregistration.module",
            ),
        ),
        migrations.AlterField(
            model_name="registration",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="registrations",
                to="users.student",
            ),
        ),
    ]
