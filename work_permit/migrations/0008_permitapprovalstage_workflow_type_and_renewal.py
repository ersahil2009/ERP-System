from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work_permit', '0007_permitrenewal'),
    ]

    operations = [
        migrations.AddField(
            model_name='permitapprovalstage',
            name='renewal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approval_stages', to='work_permit.permitrenewal'),
        ),
        migrations.AddField(
            model_name='permitapprovalstage',
            name='workflow_type',
            field=models.CharField(default='main', max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='permitapprovalstage',
            unique_together={('permit', 'workflow_type', 'renewal', 'stage')},
        ),
    ]
