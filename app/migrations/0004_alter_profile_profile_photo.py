# Generated by Django 3.2.9 on 2021-12-04 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_comment_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/', verbose_name='image'),
        ),
    ]
