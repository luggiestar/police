# Generated by Django 3.2.9 on 2022-06-10 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('POLICE', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='residency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='POLICE.district'),
        ),
    ]
