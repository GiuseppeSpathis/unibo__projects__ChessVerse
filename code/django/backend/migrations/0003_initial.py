# Generated by Django 4.2.7 on 2023-11-26 19:18

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("backend", "0002_auto_20231107_1705"),
    ]

    operations = [
        migrations.CreateModel(
            name="Guest",
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
                ("Username", models.CharField(max_length=255, unique=True)),
            ],
            options={
                "db_table": "Guest",
            },
        ),
    ]
