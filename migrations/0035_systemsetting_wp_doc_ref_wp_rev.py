from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_work_permit_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemsetting',
            name='wp_doc_ref',
            field=models.CharField(default='PTW-F-001', max_length=30, verbose_name='WP Document Reference'),
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='wp_rev',
            field=models.CharField(default='01', max_length=10, verbose_name='WP Revision Number'),
        ),
    ]
