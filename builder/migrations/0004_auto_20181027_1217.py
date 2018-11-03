# Generated by Django 2.1.1 on 2018-10-27 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('browse', '0001_initial'),
        ('builder', '0003_auto_20181023_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeckCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='browse.Card')),
            ],
        ),
        migrations.RemoveField(
            model_name='deck',
            name='cards',
        ),
        migrations.AddField(
            model_name='deck',
            name='cards',
            field=models.ManyToManyField(through='builder.DeckCard', to='browse.Card'),
        ),
        migrations.AddField(
            model_name='deckcard',
            name='deck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='builder.Deck'),
        ),
    ]