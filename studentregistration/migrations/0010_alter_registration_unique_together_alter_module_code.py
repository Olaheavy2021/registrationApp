# Generated by Django 4.2.2 on 2023-07-18 18:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("studentregistration", "0009_merge_20230712_1444"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="registration",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="module",
            name="code",
            field=models.SlugField(default="", max_length=12, unique=True),
        ),
    ]
