# Generated by Django 4.2.2 on 2023-07-18 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Audio",
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
                ("name", models.TextField(blank=True, null=True)),
                ("audio_file", models.FileField(upload_to="audio_file/")),
                ("type", models.CharField(max_length=100)),
                ("is_completed", models.BooleanField(default=False)),
                ("language", models.CharField(max_length=100)),
                ("quality_check", models.BooleanField(default=False)),
                ("content", models.TextField()),
                ("is_modified", models.BooleanField(default=False)),
                ("updated_content", models.TextField(blank=True, null=True)),
                (
                    "userId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]