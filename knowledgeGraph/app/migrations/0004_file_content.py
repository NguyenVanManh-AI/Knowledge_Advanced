# Generated by Django 5.1.2 on 2024-10-11 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_file_content_origin_file_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
