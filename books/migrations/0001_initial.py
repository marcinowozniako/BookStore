# Generated by Django 4.0.4 on 2022-05-18 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('published_year', models.CharField(max_length=12)),
                ('acquired', models.BooleanField(default=False)),
                ('thumbnail', models.URLField(blank=True)),
                ('authors', models.ManyToManyField(to='books.author')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
