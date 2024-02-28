# Generated by Django 5.0.1 on 2024-02-23 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steganography', '0004_alter_decoding_image_alter_encoding_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='decoding',
            name='type',
            field=models.CharField(default='Decoding', max_length=20),
        ),
        migrations.AddField(
            model_name='encoding',
            name='type',
            field=models.CharField(default='Encoding', max_length=20),
        ),
    ]
