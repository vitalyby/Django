# Generated by Django 2.1.4 on 2019-01-04 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_exrate', '0003_auto_20190104_1110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='valuta',
            name='id',
        ),
        migrations.AlterField(
            model_name='valuta',
            name='Cur_ID',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
