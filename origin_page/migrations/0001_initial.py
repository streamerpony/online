# Generated by Django 4.2.19 on 2025-02-07 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('file_path', models.CharField(max_length=512)),
                ('status', models.CharField(choices=[('pending', '未处理'), ('received', '已接收'), ('processed', '已处理')], default='pending', max_length=10)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
