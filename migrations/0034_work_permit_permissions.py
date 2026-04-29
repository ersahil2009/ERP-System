from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_daily_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='perm_wp_view',
            field=models.BooleanField(default=True, verbose_name='WP View'),
        ),
        migrations.AddField(
            model_name='employee',
            name='perm_wp_write',
            field=models.BooleanField(default=True, verbose_name='WP Write'),
        ),
        migrations.AddField(
            model_name='employee',
            name='perm_wp_approve',
            field=models.BooleanField(default=False, verbose_name='WP Approve/Reject'),
        ),
        migrations.AddField(
            model_name='employee',
            name='perm_wp_delete',
            field=models.BooleanField(default=False, verbose_name='WP Delete'),
        ),
        migrations.AddField(
            model_name='employee',
            name='perm_wp_report',
            field=models.BooleanField(default=False, verbose_name='WP Reports'),
        ),
    ]
