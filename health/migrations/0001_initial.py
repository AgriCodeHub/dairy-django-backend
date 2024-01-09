# Generated by Django 5.0 on 2024-01-09 07:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiseaseCategory",
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
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("Nutrition", "Nutrition"),
                            ("Infectious", "Infectious"),
                            ("Physiological", "Physiological"),
                            ("Genetic", "Genetic"),
                        ],
                        max_length=15,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Pathogen",
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
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("Bacteria", "Bacteria"),
                            ("Virus", "Virus"),
                            ("Fungi", "Fungi"),
                            ("Unknown", "Unknown"),
                        ],
                        max_length=10,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Symptoms",
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
                ("name", models.CharField(max_length=50)),
                (
                    "symptom_type",
                    models.CharField(
                        choices=[
                            ("Respiratory", "Respiratory"),
                            ("Digestive", "Digestive"),
                            ("Reproductive", "Reproductive"),
                            ("Physical", "Physical"),
                            ("Musculoskeletal", "Musculoskeletal"),
                            ("Metabolic", "Metabolic"),
                            ("Other", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("description", models.TextField(null=True)),
                (
                    "severity",
                    models.CharField(
                        choices=[
                            ("Mild", "Mild"),
                            ("Moderate", "Moderate"),
                            ("Severe", "Severe"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        choices=[
                            ("Head", "Head"),
                            ("Neck", "Neck"),
                            ("Chest", "Chest"),
                            ("Abdomen", "Abdomen"),
                            ("Back", "Back"),
                            ("Legs", "Legs"),
                            ("Tail", "Tail"),
                            ("Whole body", "Whole Body"),
                            ("Other", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("date_observed", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="CullingRecord",
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
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("Injuries", "Injuries"),
                            ("Chronic Health Issues", "Chronic Health"),
                            ("Cost Of Care", "Cost Of Care"),
                            ("Unprofitable", "Unprofitable"),
                            ("Low Market Demand", "Low Market Demand"),
                            ("Age", "Age"),
                            ("Consistent Low Production", "Consistent Low Production"),
                            ("Low Quality", "Consistent Poor Quality"),
                            (
                                "Inefficient Feed Conversion",
                                "Inefficient Feed Conversion",
                            ),
                            ("Inherited Diseases", "Inherited Diseases"),
                            ("Inbreeding", "Inbreeding"),
                            ("Unwanted Traits", "Unwanted Traits"),
                            ("Climate Change", "Climate Change"),
                            ("Natural Disaster", "Natural Disaster"),
                            ("Overpopulation", "Overpopulation"),
                            ("Government Regulations", "Government Regulations"),
                            ("Animal Welfare Standards", "Animal Welfare Standards"),
                            (
                                "Environmental Protection Laws",
                                "Environment Protection Laws",
                            ),
                        ],
                        max_length=35,
                    ),
                ),
                ("notes", models.TextField(max_length=100, null=True)),
                ("date_carried", models.DateField(auto_now_add=True)),
                (
                    "cow",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="culling_record",
                        to="core.cow",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuarantineRecord",
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
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("Sick Cow", "Sick Cow"),
                            ("Bought Cow", "Bought Cow"),
                            ("New Cow", "New Cow"),
                            ("Calving", "Calving"),
                        ],
                        max_length=35,
                    ),
                ),
                ("start_date", models.DateField(auto_now_add=True)),
                ("end_date", models.DateField(null=True)),
                ("notes", models.TextField(max_length=100, null=True)),
                (
                    "cow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quarantine_records",
                        to="core.cow",
                    ),
                ),
            ],
            options={
                "get_latest_by": "-start_date",
            },
        ),
        migrations.CreateModel(
            name="WeightRecord",
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
                ("weight_in_kgs", models.DecimalField(decimal_places=2, max_digits=6)),
                ("date_taken", models.DateField(auto_now_add=True)),
                (
                    "cow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.cow"
                    ),
                ),
            ],
        ),
    ]
