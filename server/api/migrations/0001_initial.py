# Generated by Django 5.1.2 on 2024-10-17 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open', models.DecimalField(decimal_places=4, max_digits=10)),
                ('high', models.DecimalField(decimal_places=4, max_digits=10)),
                ('low', models.DecimalField(decimal_places=4, max_digits=10)),
                ('close', models.DecimalField(decimal_places=4, max_digits=10)),
                ('volume', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
    ]
