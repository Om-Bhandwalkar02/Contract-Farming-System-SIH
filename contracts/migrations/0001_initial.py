# Generated by Django 5.1.1 on 2024-09-22 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('delivery_address', models.CharField(max_length=255)),
                ('delivery_handler', models.CharField(max_length=255)),
                ('delivery_date', models.DateField()),
                ('signed_by_farmer', models.BooleanField(default=False)),
                ('signed_by_buyer', models.BooleanField(default=False)),
                ('farmer_signed_at', models.DateTimeField(blank=True, null=True)),
                ('buyer_signed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
