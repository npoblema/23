# Generated by Django 3.2.25 on 2025-04-08 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0002_auto_20250404_1906'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='habit',
            options={},
        ),
        migrations.AlterField(
            model_name='habit',
            name='action',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='habit',
            name='place',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='habit',
            name='reward',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
