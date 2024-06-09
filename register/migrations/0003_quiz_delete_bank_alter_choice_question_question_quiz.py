# Generated by Django 5.0.3 on 2024-06-09 14:58

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("register", "0002_bank"),
    ]

    operations = [
        migrations.CreateModel(
            name="Quiz",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "code",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Bank",
        ),
        migrations.AlterField(
            model_name="choice",
            name="question",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="register.question",
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="quiz",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="register.quiz",
            ),
            preserve_default=False,
        ),
    ]
