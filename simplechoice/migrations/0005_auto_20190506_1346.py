# Generated by Django 2.2 on 2019-05-06 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simplechoice', '0004_auto_20190506_1138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ('-updated_at',)},
        ),
        migrations.AddField(
            model_name='game',
            name='ranking',
            field=models.IntegerField(default=0),
        ),
    ]
