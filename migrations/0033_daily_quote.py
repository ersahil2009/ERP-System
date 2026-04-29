from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_perm_reports_grv'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyQuote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_number', models.PositiveSmallIntegerField(help_text='1–365', unique=True)),
                ('quote', models.TextField()),
                ('author', models.CharField(blank=True, max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Daily Quote',
                'ordering': ['day_number'],
            },
        ),
    ]
