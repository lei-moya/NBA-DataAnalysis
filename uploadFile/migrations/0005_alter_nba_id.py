# Generated by Django 5.1.3 on 2024-11-19 16:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("uploadFile", "0004_alter_nba_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nba",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
