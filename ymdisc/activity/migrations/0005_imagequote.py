# Generated by Django 2.1.5 on 2019-01-17 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_remove_activity_open'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageQuote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.FileField(upload_to='')),
            ],
        ),
    ]
