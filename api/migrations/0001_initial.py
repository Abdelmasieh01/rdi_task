# Generated by Django 5.1.4 on 2025-01-05 20:32

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('file', models.ImageField(upload_to='images/', verbose_name='Image Url')),
                ('width', models.PositiveSmallIntegerField(verbose_name='Image width')),
                ('height', models.PositiveSmallIntegerField(verbose_name='Image height')),
                ('channels', models.PositiveBigIntegerField(verbose_name='Number of channels')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pdf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='PDFs/', validators=[api.models.validate_pdf_type], verbose_name='File Url')),
                ('page_count', models.PositiveSmallIntegerField(verbose_name='Number of pages')),
                ('width', models.PositiveSmallIntegerField(verbose_name='Page width')),
                ('height', models.PositiveSmallIntegerField(verbose_name='Page height')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]