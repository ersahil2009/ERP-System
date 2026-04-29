from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_permit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workpermit',
            name='moc_required',
            field=models.BooleanField(default=False, verbose_name='MOC (Management of Change) Required'),
        ),
    ]
