# Generated by Django 5.0.3 on 2024-06-17 13:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0006_alter_quiz_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="date_created",
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(
                    2024, 6, 17, 13, 45, 56, 606362, tzinfo=datetime.timezone.utc
                ),
            ),
            preserve_default=False,
        ),
    ]