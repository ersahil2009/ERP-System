from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_permit', '0005_remove_end_datetime_add_renewal'),
    ]

    operations = [
        migrations.AddField(
            model_name='permitapprovalstage',
            name='stage_type',
            field=models.CharField(default='approval', max_length=20),
        ),
    ]
