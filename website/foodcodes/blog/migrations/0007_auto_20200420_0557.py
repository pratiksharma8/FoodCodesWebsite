# Generated by Django 3.0.5 on 2020-04-20 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_delete_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='comment',
        ),
    ]
