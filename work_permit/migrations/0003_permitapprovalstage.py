import django.db.models.deletion
import secrets
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_permit', '0002_workpermit_moc_required'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PermitApprovalStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.PositiveSmallIntegerField()),
                ('stage_label', models.CharField(max_length=120)),
                ('approver_role', models.CharField(max_length=30)),
                ('approver_dept', models.CharField(blank=True, max_length=100)),
                ('approver_desig', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('remarks', models.TextField(blank=True)),
                ('token', models.CharField(blank=True, max_length=64, null=True, unique=True)),
                ('acted_at', models.DateTimeField(blank=True, null=True)),
                ('approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wp_stage_approvals', to=settings.AUTH_USER_MODEL)),
                ('permit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_stages', to='work_permit.workpermit')),
            ],
            options={'ordering': ['stage'], 'unique_together': {('permit', 'stage')}},
        ),
    ]
