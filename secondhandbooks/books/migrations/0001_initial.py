# Generated by Django 3.0.1 on 2022-11-05 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('details', models.CharField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('friendly_name', models.CharField(
                    blank=True, max_length=254, null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(blank=True, max_length=254, null=True)),
                ('name', models.CharField(max_length=254)),
                ('description', models.TextField()),
                ('special', models.BooleanField(
                    blank=True, default=False, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('amount', models.IntegerField(blank=True, default=0, null=True)),
                ('rating', models.DecimalField(blank=True,
                 decimal_places=2, max_digits=6, null=True)),
                ('image_url', models.URLField(
                    blank=True, max_length=1024, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('author', models.ForeignKey(blank=True, null=True,
                 on_delete=django.db.models.deletion.SET_NULL, to='books.Author')),
                ('category', models.ForeignKey(blank=True, null=True,
                 on_delete=django.db.models.deletion.SET_NULL, to='books.Category')),
            ],
        ),
    ]
