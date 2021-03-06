# Generated by Django 3.2 on 2022-01-04 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookTest', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='create_time',
            new_name='createTime',
        ),
        migrations.AddField(
            model_name='book',
            name='isSell',
            field=models.BooleanField(default=False, null=True, verbose_name='是否可卖'),
        ),
        migrations.AddField(
            model_name='book',
            name='read',
            field=models.IntegerField(default=0, null=True, verbose_name='阅读量'),
        ),
    ]
