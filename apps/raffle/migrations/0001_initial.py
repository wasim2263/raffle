# Generated by Django 3.2.18 on 2023-04-07 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Raffle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('total_tickets', models.PositiveIntegerField()),
                ('remaining_tickets', models.PositiveIntegerField()),
                ('verification_codes', models.JSONField(default=dict)),
                ('winners_drawn', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.PositiveIntegerField()),
                ('raffle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='raffle.raffle')),
            ],
        ),
    ]