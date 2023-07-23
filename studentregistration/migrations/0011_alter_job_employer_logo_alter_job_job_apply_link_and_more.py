# Generated by Django 4.2.2 on 2023-07-22 19:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("studentregistration", "0010_job_alter_registration_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="employer_logo",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="job_apply_link",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="job_city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="job_country",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="job_description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="job_title",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
