# Generated by Django 4.1.7 on 2023-02-20 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Hyperlink",
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
                ("url", models.CharField(max_length=200)),
                ("origin", models.CharField(max_length=200)),
                ("date_discovered", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
