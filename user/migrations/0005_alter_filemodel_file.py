# Generated by Django 3.2 on 2022-01-12 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_filemodel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='file',
            field=models.FileField(upload_to='static/%Y/%m/%d/'),
        ),
    ]
