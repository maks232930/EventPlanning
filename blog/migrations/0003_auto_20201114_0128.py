# Generated by Django 3.1 on 2020-11-13 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20201114_0105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='subject',
        ),
        migrations.AddField(
            model_name='comment',
            name='surname',
            field=models.CharField(blank=True, max_length=50, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Имя'),
        ),
    ]
