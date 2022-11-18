# Generated by Django 4.0.7 on 2022-11-09 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commontype', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Photo File Name')),
                ('ext', models.CharField(max_length=10, verbose_name='Photo File Extend')),
                ('path', models.CharField(max_length=255, verbose_name='Photo File Path')),
                ('commontype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commontype.commontype', verbose_name='Photo Type')),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photo',
            },
        ),
    ]
