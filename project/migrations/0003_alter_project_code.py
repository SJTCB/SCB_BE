# Generated by Django 5.1.3 on 2024-11-13 16:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0002_alter_project_team_members"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="code",
            field=models.FileField(upload_to=""),
        ),
    ]
