# Generated by Django 5.0.3 on 2024-06-12 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="choice",
            name="question",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="question_choices",
                to="api.question",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="quiz",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="quiz_questions",
                to="api.quiz",
            ),
        ),
    ]