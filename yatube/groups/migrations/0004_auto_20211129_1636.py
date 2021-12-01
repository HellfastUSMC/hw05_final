# Generated by Django 2.2.16 on 2021-11-29 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20211022_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(help_text='Введите описание группы', verbose_name='Описание группы'),
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(help_text='Введите адрес группы', unique=True, verbose_name='Адрес группы'),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(help_text='Введите название группы', max_length=200, verbose_name='Название группы'),
        ),
    ]