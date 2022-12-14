# Generated by Django 3.2.4 on 2022-08-20 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Products",
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
                ("name", models.CharField(max_length=255)),
                ("brand", models.CharField(max_length=255)),
                (
                    "unit",
                    models.CharField(
                        choices=[("PCS", "PCS"), ("PCK", "PCK")],
                        default="PCS",
                        max_length=140,
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                ("barcode", models.CharField(blank=True, max_length=50, null=True)),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
