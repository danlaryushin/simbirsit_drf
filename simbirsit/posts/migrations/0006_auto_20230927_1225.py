# Generated by Django 2.2.19 on 2023-09-27 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20230927_1148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-is_available', '-pub_date'), 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='status',
            new_name='is_available',
        ),
    ]
