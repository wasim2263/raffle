# Generated by Django 3.2.18 on 2023-04-08 01:07

from django.db import migrations
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('raffle_draw', '0002_auto_20230408_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prize',
            name='id',
            field=model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='raffle',
            name='id',
            field=model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='id',
            field=model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
