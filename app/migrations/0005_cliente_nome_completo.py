# Generated by Django 5.1.3 on 2024-12-05 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_categoria_produto_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='nome_completo',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
