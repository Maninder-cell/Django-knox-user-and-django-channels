# Generated by Django 3.1.2 on 2020-12-09 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0002_note_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['-done']},
        ),
    ]
