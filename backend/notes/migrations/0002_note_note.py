# Generated by Django 5.1.4 on 2024-12-11 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='note',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
