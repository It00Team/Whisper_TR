# Generated by Django 4.2.4 on 2023-08-16 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manual', '0010_alter_myaudiomain_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myaudiomain',
            old_name='audio_file',
            new_name='audioFile',
        ),
        migrations.RenameField(
            model_name='myaudiomain',
            old_name='name',
            new_name='filename',
        ),
    ]
