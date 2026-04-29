from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_permit', '0003_permitapprovalstage'),
    ]

    operations = [
        migrations.AddField(
            model_name='workpermit',
            name='moc_details',
            field=models.TextField(blank=True, verbose_name='MOC Details'),
        ),
    ]
