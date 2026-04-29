from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_permit', '0004_workpermit_moc_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workpermit',
            name='end_datetime',
        ),
        migrations.AddField(
            model_name='workpermit',
            name='renewal_required',
            field=models.BooleanField(default=False, verbose_name='Permit Renewal Required'),
        ),
    ]
