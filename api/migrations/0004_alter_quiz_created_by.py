# Generated by Django 5.0.3 on 2024-06-16 13:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_quiz_created_by"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="created_by",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_questions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
