# Generated by Django 4.0.4 on 2022-05-02 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20220501_1928'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transactionrecord',
        ),
        migrations.AlterModelOptions(
            name='class',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='corn',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='dcboard',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='feedback',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='futures',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='history',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='indexclass',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='intelligentstrategy',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='member',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='minidow',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='mininastaq',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='minirussell',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='minisp',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='mtx',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='newscontent',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='soy',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='te',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='technicalstrategry',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='tf',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='tx',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='wheat',
            options={'managed': True},
        ),
    ]
