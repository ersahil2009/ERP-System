from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('work_permit', '0006_permitapprovalstage_stage_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PermitRenewal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('renewal_no', models.PositiveSmallIntegerField()),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('valid_from', models.DateTimeField(blank=True, null=True)),
                ('valid_until', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('permit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name='renewals', to='work_permit.workpermit')),
                ('requested_by', models.ForeignKey(blank=True, null=True,
                                                   on_delete=django.db.models.deletion.SET_NULL,
                                                   related_name='permit_renewals_requested',
                                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['renewal_no']},
        ),
    ]
