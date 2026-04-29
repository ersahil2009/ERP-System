from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_new_permissions_and_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='perm_reports_grv',
            field=models.BooleanField(default=False, verbose_name='GRV Reports View'),
        ),
        migrations.AddField(
            model_name='rolepermissiontemplate',
            name='perm_reports_grv',
            field=models.BooleanField(default=False),
        ),
    ]
