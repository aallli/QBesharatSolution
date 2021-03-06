# Generated by Django 3.0.6 on 2020-07-18 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QBesharat', '0007_concepts_memorizer_qari_tutor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000, unique=True, verbose_name='Topic')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
                'ordering': ['name'],
            },
        ),
    ]
