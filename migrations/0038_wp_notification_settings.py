from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_merge_wp_migrations'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemsetting',
            name='notif_wp_popup',
            field=models.BooleanField(default=True, verbose_name='WP Popup Notifications'),
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='notif_wp_email',
            field=models.BooleanField(default=True, verbose_name='WP Email Notifications'),
        ),
    ]
