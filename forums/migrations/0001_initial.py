# Generated by Django 3.2.9 on 2022-06-07 19:08

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
            name='ForumTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('active', models.BooleanField(default=True)),
                ('locked', models.BooleanField(default=False)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('views', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_text', models.TextField()),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(default=None)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forumpost', to='forums.forumtopic')),
                ('post_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userpost', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
