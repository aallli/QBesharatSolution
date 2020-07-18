# Generated by Django 3.0.6 on 2020-07-18 12:30

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('QBesharat', '0010_network'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, default='1360-01-01', null=True, verbose_name='Birth Date'),
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, unique=True, verbose_name='Name')),
                ('poster', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=75, size=[500, 500], upload_to='media/', verbose_name='Poster')),
                ('count', models.IntegerField(default=60, verbose_name='Count')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('network', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='QBesharat.Network', verbose_name='Network')),
            ],
            options={
                'verbose_name': 'Program',
                'verbose_name_plural': 'Programs',
                'ordering': ['name'],
            },
        ),
    ]