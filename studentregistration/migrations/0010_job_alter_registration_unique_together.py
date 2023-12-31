# Generated by Django 4.2.2 on 2023-07-22 11:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("studentregistration", "0009_merge_20230712_1444"),
    ]

    operations = [
        migrations.CreateModel(
            name="Job",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("employer_name", models.CharField(max_length=100)),
                ("employer_logo", models.URLField()),
                ("job_employment_type", models.CharField(max_length=20)),
                ("job_title", models.CharField(max_length=200)),
                ("job_apply_link", models.URLField()),
                ("job_description", models.TextField()),
                ("job_city", models.CharField(max_length=100)),
                ("job_country", models.CharField(max_length=15)),
            ],
            options={
                "verbose_name": "Job",
                "verbose_name_plural": "Jobs",
            },
        ),
        migrations.AlterUniqueTogether(
            name="registration",
            unique_together=set(),
        ),
    ]
