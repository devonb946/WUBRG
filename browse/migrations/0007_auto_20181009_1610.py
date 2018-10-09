# Generated by Django 2.1 on 2018-10-09 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('browse', '0006_auto_20180930_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='image_uris',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small', models.URLField()),
                ('normal', models.URLField()),
                ('large', models.URLField()),
                ('png', models.URLField()),
                ('art_crop', models.URLField()),
                ('border_crop', models.URLField()),
            ],
        ),
        migrations.RemoveField(
            model_name='card',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='card',
            name='border_color',
        ),
        migrations.RemoveField(
            model_name='card',
            name='cmc',
        ),
        migrations.RemoveField(
            model_name='card',
            name='flavor_text',
        ),
        migrations.RemoveField(
            model_name='card',
            name='frame',
        ),
        migrations.RemoveField(
            model_name='card',
            name='image',
        ),
        migrations.RemoveField(
            model_name='card',
            name='layout',
        ),
        migrations.RemoveField(
            model_name='card',
            name='loyalty',
        ),
        migrations.RemoveField(
            model_name='card',
            name='mana_cost',
        ),
        migrations.RemoveField(
            model_name='card',
            name='oracle_text',
        ),
        migrations.RemoveField(
            model_name='card',
            name='power',
        ),
        migrations.RemoveField(
            model_name='card',
            name='rarity',
        ),
        migrations.RemoveField(
            model_name='card',
            name='reserved',
        ),
        migrations.RemoveField(
            model_name='card',
            name='set_abbr',
        ),
        migrations.RemoveField(
            model_name='card',
            name='set_name',
        ),
        migrations.RemoveField(
            model_name='card',
            name='toughness',
        ),
        migrations.RemoveField(
            model_name='card',
            name='type_line',
        ),
        migrations.AddField(
            model_name='card',
            name='set',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
