# Generated by Django 4.2.3 on 2023-07-15 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Date that the task was create', verbose_name='Creation date'),
        ),
    ]