# Generated by Django 4.0.7 on 2022-11-09 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commontype', '0001_initial'),
        ('photoes', '0001_initial'),
        ('actors', '0001_initial'),
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Movie Name')),
                ('provider', models.CharField(max_length=100, null=True, verbose_name='Movie Provider')),
                ('file_path', models.CharField(max_length=255, verbose_name='Movie File Path')),
                ('actors', models.ManyToManyField(to='actors.actor', verbose_name='Actors of Movie')),
                ('movie_images', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photoes.photo', verbose_name='Movie Images')),
                ('movie_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commontype.commontype', verbose_name='Movie Type')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.storage', verbose_name='Movie Storage Item')),
            ],
            options={
                'verbose_name': 'Movie',
                'verbose_name_plural': 'Movie',
            },
        ),
    ]