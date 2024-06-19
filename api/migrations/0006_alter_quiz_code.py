# Generated by Django 5.0.3 on 2024-06-16 16:48

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0005_alter_quiz_created_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="code",
            field=models.CharField(
                default=api.models.generate_unique_alphanumeric_code,
                editable=False,
                max_length=6,
                unique=True,
            ),
        ),
    ]