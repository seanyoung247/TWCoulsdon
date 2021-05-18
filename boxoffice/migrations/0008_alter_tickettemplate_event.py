# Generated by Django 3.2 on 2021-05-17 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_venue_capacity'),
        ('boxoffice', '0007_alter_tickettemplate_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickettemplate',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_template', to='events.event'),
        ),
    ]