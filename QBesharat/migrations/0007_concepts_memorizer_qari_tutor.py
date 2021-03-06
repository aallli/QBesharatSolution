# Generated by Django 3.0.6 on 2020-06-28 10:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QBesharat', '0006_auto_20200626_2019'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Grade')),
                ('course_duration', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(400)], verbose_name='Course duration')),
                ('course_content', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Course Content')),
                ('courses', models.CharField(blank=True, max_length=500, null=True, verbose_name='Courses')),
                ('awards', models.CharField(blank=True, max_length=500, null=True, verbose_name='Awards')),
                ('certificates', models.CharField(blank=True, max_length=500, null=True, verbose_name='Certificates')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Tutor skill')),
            ],
            options={
                'verbose_name': 'Tutor skill',
                'verbose_name_plural': 'Tutors skill',
            },
        ),
        migrations.CreateModel(
            name='Qari',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fluent_reading', models.BooleanField(blank=True, null=True, verbose_name='Fluent Reading')),
                ('tahdir', models.BooleanField(blank=True, null=True, verbose_name='Tahdir')),
                ('tartil', models.BooleanField(blank=True, null=True, verbose_name='Tartil')),
                ('research', models.BooleanField(blank=True, null=True, verbose_name='Research')),
                ('courses', models.CharField(blank=True, max_length=500, null=True, verbose_name='Courses')),
                ('awards', models.CharField(blank=True, max_length=500, null=True, verbose_name='Awards')),
                ('certificates', models.CharField(blank=True, max_length=500, null=True, verbose_name='Certificates')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Qari skill')),
            ],
            options={
                'verbose_name': 'Qari skill',
                'verbose_name_plural': 'Qari skill',
            },
        ),
        migrations.CreateModel(
            name='Memorizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parts', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='Parts')),
                ('awards', models.CharField(blank=True, max_length=500, null=True, verbose_name='Awards')),
                ('certificates', models.CharField(blank=True, max_length=500, null=True, verbose_name='Certificates')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Memorizer skill')),
            ],
            options={
                'verbose_name': 'Memorizer skill',
                'verbose_name_plural': 'Memorizers skill',
            },
        ),
        migrations.CreateModel(
            name='Concepts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interpretation', models.BooleanField(blank=True, null=True, verbose_name='Interpretation')),
                ('translation', models.BooleanField(blank=True, null=True, verbose_name='Translation')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Concepts skill')),
            ],
            options={
                'verbose_name': 'Concepts skill',
                'verbose_name_plural': 'Concepts skill',
            },
        ),
    ]
