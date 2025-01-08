# Generated by Django 5.1.3 on 2025-01-06 00:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_categoria_cliente_proveedor_mueble_imagen_venta_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mueble',
            old_name='precio',
            new_name='precio_original',
        ),
        migrations.AddField(
            model_name='mueble',
            name='descuento',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='mueble',
            name='popularidad',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Critica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion', models.PositiveIntegerField()),
                ('comentario', models.TextField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.cliente')),
                ('mueble', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criticas', to='app1.mueble')),
            ],
            options={
                'db_table': 'Critica',
                'ordering': ['-fecha'],
            },
        ),
    ]
