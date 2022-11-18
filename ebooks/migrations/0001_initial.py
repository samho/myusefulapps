# Generated by Django 4.0.7 on 2022-11-09 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commontype', '0001_initial'),
        ('actors', '0001_initial'),
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='EBook Name')),
                ('file_path', models.CharField(max_length=500, verbose_name='EBook File Path')),
                ('actors', models.ManyToManyField(to='actors.actor', verbose_name='Actors of EBook')),
                ('ebook_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commontype.commontype', verbose_name='EBook Type')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.storage', verbose_name='EBook Storage')),
            ],
            options={
                'verbose_name': 'Ebooks',
                'verbose_name_plural': 'Ebooks',
            },
        ),
    ]