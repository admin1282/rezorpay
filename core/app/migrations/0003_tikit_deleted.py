# Generated by Django 5.0.4 on 2024-04-18 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_tikit_created_tikit_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='tikit',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]