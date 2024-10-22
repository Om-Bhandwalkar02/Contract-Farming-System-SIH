# Generated by Django 5.1.1 on 2024-09-22 16:15

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='IN', unique=True)),
                ('full_name', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('farmer', 'Farmer'), ('buyer', 'Buyer')], max_length=10)),
                ('aadhar_number', models.CharField(max_length=12, unique=True)),
                ('aadhar_certificate', models.FileField(upload_to='media/aadhar/')),
                ('farmer_certificate', models.FileField(blank=True, null=True, upload_to='media/certificates/')),
                ('buyer_certificate', models.FileField(blank=True, null=True, upload_to='media/certificates/')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='media/profile_pictures/')),
                ('address', models.CharField(max_length=255)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
