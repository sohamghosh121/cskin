# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cskin.models


class Migration(migrations.Migration):

    dependencies = [
        ('cskin', '0002_auto_20150927_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=models.ImageField(upload_to=cskin.models.image_directory_path),
        ),
    ]
