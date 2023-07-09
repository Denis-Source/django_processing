# Generated by Django 4.2.3 on 2023-07-08 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='Email of the user', max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, help_text='User profile picture', null=True, upload_to='user_images', verbose_name='Profile image'),
        ),
        migrations.AlterField(
            model_name='user',
            name='registered',
            field=models.DateTimeField(auto_now_add=True, help_text='Automatically generated date and time of user registration', verbose_name='Registered date'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('staff', 'Staff'), ('admin', 'Admin')], default='user', help_text="User assigned role, regular 'user' is by default", max_length=8, verbose_name='User role'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='The main distinguishing field', max_length=64, unique=True, verbose_name='Username'),
        ),
    ]
