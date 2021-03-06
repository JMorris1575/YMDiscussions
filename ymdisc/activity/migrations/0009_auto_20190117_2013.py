# Generated by Django 2.1.5 on 2019-01-18 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0008_section_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='item',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.AddField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='activity.Item'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
