# Generated by Django 4.1.2 on 2022-11-03 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_pharmacist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('itemprice_per_strip', models.PositiveIntegerField(null=True)),
                ('description', models.CharField(max_length=200)),
                ('quantity_in_strip', models.PositiveIntegerField(null=True)),
                ('manufractureDate', models.DateField()),
                ('expirayDate', models.DateField()),
            ],
        ),
    ]