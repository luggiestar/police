# Generated by Django 3.2.9 on 2022-06-12 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('POLICE', '0003_alter_user_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('week_number', models.CharField(blank=True, max_length=2)),
                ('finish_date', models.DateField(blank=True, null=True)),
                ('complaint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaint_tracking', to='POLICE.complainant')),
                ('crime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='POLICE.crime')),
            ],
        ),
    ]
