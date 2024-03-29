# Generated by Django 4.2.7 on 2024-01-11 07:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emotion', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'emotions',
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'stories',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=30)),
                ('firstname', models.CharField(max_length=30)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='AnalyzedStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analyzed_emotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.emotion')),
                ('phrase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.story')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.users')),
            ],
            options={
                'verbose_name_plural': 'analyzed stories',
            },
        ),
    ]
