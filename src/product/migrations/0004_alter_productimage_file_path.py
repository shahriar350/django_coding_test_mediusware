# Generated by Django 4.0.3 on 2022-03-15 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_productvariantprice_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='file_path',
            field=models.ImageField(upload_to=''),
        ),
    ]