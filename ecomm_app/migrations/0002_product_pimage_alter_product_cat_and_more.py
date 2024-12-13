# Generated by Django 5.1.3 on 2024-12-06 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pimage',
            field=models.ImageField(default=0, upload_to='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='cat',
            field=models.IntegerField(choices=[(1, 'Mobile'), (2, 'Shoes'), (3, 'Clothes'), (4, 'Bags')], verbose_name='Categories'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Available'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pdetails',
            field=models.CharField(max_length=200, verbose_name='Product Details'),
        ),
    ]
