# Generated by Django 5.0.4 on 2024-11-25 14:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0004_remove_project_code_filename"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="zip_content",
            field=models.TextField(blank=True),
        ),
    ]