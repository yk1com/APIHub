# Generated by Django 5.0 on 2024-03-23 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('file_name', models.CharField(max_length=255)),
                ('download_link', models.CharField(max_length=255)),
            ],
        ),
    ]
