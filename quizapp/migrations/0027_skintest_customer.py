# Generated by Django 3.1.3 on 2020-12-07 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0026_remove_skintest_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='skintest',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='quizapp.customer'),
        ),
    ]
