# Generated by Django 4.2.16 on 2024-11-09 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0006_alter_graperegion_country_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graperegion',
            name='country_code',
            field=models.CharField(blank=True, help_text='Country code', max_length=5),
        ),
        migrations.RemoveField(
            model_name='winepreference',
            name='grape_region',
        ),
        migrations.AddField(
            model_name='winepreference',
            name='grape_region',
            field=models.ManyToManyField(related_name='preferences', to='preferences.graperegion'),
        ),
    ]
