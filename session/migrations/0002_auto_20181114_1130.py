# Generated by Django 2.1.3 on 2018-11-14 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='created',
        ),
        migrations.AddField(
            model_name='file',
            name='title',
            field=models.CharField(default='default', max_length=100, verbose_name='title'),
        ),
    ]
