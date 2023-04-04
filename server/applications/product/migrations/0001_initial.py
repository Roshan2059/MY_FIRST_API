# Generated by Django 4.0.8 on 2023-04-04 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('design_no', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('material', models.CharField(max_length=255)),
                ('usage_of_material', models.TextField()),
                ('sewing_wages', models.DecimalField(decimal_places=2, max_digits=10)),
                ('master_charge', models.DecimalField(decimal_places=2, max_digits=10)),
                ('washing_charges', models.DecimalField(decimal_places=2, max_digits=10)),
                ('button_charges', models.DecimalField(decimal_places=2, max_digits=10)),
                ('packing_charges', models.DecimalField(decimal_places=2, max_digits=10)),
                ('zipper_charges', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='product_images')),
                ('thumbnail', models.ImageField(upload_to='product_thumbnails')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
