# Generated by Django 4.2.7 on 2023-12-14 16:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0009_remove_registeredusers_gamedraw_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="MultiplayerLeaderboard",
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
                ("username", models.CharField(max_length=255)),
                ("elo", models.PositiveIntegerField()),
            ],
            options={
                "ordering": ["-elo"],
            },
        ),
        migrations.AlterModelOptions(
            name="dailyleaderboard",
            options={"ordering": ["moves_count"]},
        ),
        migrations.AlterModelOptions(
            name="weeklyleaderboard",
            options={"ordering": ["moves_count"]},
        ),
    ]