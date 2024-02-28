# Generated by Django 5.0.1 on 2024-02-23 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steganography', '0002_remove_encoding_password_decoding_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decoding',
            name='image',
            field=models.ImageField(upload_to='steganography/media/decodings/'),
        ),
        migrations.AlterField(
            model_name='encoding',
            name='image',
            field=models.ImageField(upload_to='steganography/media/encodings/'),
        ),
    ]