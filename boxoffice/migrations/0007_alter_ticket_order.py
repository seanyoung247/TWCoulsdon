# Generated by Django 3.2 on 2021-05-26 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boxoffice', '0006_alter_ticket_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='boxoffice.order'),
        ),
    ]