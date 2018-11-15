# Generated by Django 2.1.3 on 2018-11-15 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0003_auto_20181114_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bad_day', models.DateField()),
                ('comm', models.TextField()),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CSV_file', to='session.CSVFile')),
            ],
        ),
    ]
