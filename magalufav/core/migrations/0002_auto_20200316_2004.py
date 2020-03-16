# Generated by Django 3.0.4 on 2020-03-16 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Produto',
        ),
        migrations.AddField(
            model_name='favorito',
            name='id_produto',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='favorito',
            unique_together={('cliente', 'id_produto')},
        ),
    ]