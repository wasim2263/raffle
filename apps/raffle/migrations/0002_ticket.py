# Generated by Django 3.2.18 on 2023-04-07 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('raffle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_number', models.PositiveIntegerField()),
                ('verification_code', models.CharField(blank=True, max_length=100, null=True)),
                ('ip_address', models.CharField(max_length=255)),
                ('prize', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='raffle.prize')),
                ('raffle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='raffle.raffle')),
            ],
            options={
                'unique_together': {('raffle', 'verification_code')},
            },
        ),
    ]
