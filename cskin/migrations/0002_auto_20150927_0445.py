# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cskin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('details', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='image',
            name='date_taken',
        ),
        migrations.RemoveField(
            model_name='image',
            name='patient',
        ),
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=models.ImageField(upload_to=b'patient_images/'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
        ),
        migrations.AddField(
            model_name='session',
            name='patient',
            field=models.ForeignKey(related_name='patient', to='cskin.Patient'),
        ),
        migrations.AddField(
            model_name='image',
            name='session',
            field=models.ForeignKey(related_name='session', default=1, to='cskin.Session'),
            preserve_default=False,
        ),
    ]
