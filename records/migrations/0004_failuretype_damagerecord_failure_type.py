# Generated by Django 5.1.6 on 2025-02-18 04:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_damagerecord_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='FailureType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='damagerecord',
            name='failure_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='records.failuretype'),
        ),
    ]
