# Generated by Django 2.1.1 on 2018-10-21 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='card_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='deck',
            name='description',
            field=models.CharField(default='', max_length=10000),
        ),
        migrations.AlterField(
            model_name='deck',
            name='colors',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='deck',
            name='creator',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='deck',
            name='format',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='deck',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
