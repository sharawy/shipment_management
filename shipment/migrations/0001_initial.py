# Generated by Django 4.1.1 on 2022-09-10 22:21

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('tracking_number', models.CharField(blank=True, max_length=255)),
                ('weight', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('no_of_items', models.PositiveIntegerField(default=1)),
                ('description', models.TextField(blank=True, default='')),
                ('provider', models.CharField(blank=True, max_length=256)),
                ('provider_response', models.TextField(blank=True, null=True)),
                ('label_url', models.TextField(blank=True, null=True)),
                ('from_address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sender_address', to='providers.address')),
                ('to_address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='receiver_address', to='providers.address')),
                ('tracking_events', models.ManyToManyField(to='providers.trackingevent')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]