from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkPermit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permit_number', models.CharField(editable=False, max_length=30, unique=True)),
                ('permit_type', models.CharField(choices=[('hot_work', 'Hot Work Permit'), ('cold_work', 'Cold Work Permit'), ('height_work', 'Work at Height Permit'), ('confined_space', 'Confined Space Entry Permit'), ('electrical', 'Electrical Isolation Permit'), ('excavation', 'Excavation / Digging Permit'), ('radiography', 'Radiography / X-Ray Permit'), ('chemical', 'Chemical Handling Permit'), ('crane_lifting', 'Crane & Lifting Operations Permit'), ('demolition', 'Demolition Permit'), ('pressure_test', 'Pressure Testing Permit'), ('vehicle_entry', 'Vehicle Entry Permit')], max_length=30)),
                ('title', models.CharField(max_length=200, verbose_name='Work Description / Title')),
                ('location', models.CharField(max_length=200, verbose_name='Work Location / Area')),
                ('equipment_tag', models.CharField(blank=True, max_length=100, verbose_name='Equipment / Tag No.')),
                ('plant_area', models.CharField(blank=True, max_length=100, verbose_name='Plant Area / Unit')),
                ('start_datetime', models.DateTimeField(verbose_name='Planned Start Date & Time')),
                ('end_datetime', models.DateTimeField(verbose_name='Planned End Date & Time')),
                ('shift', models.CharField(blank=True, choices=[('A', 'A Shift (06:00–14:00)'), ('B', 'B Shift (14:00–22:00)'), ('C', 'C Shift (22:00–06:00)'), ('G', 'General Shift (08:00–17:00)')], max_length=2)),
                ('actual_start', models.DateTimeField(blank=True, null=True)),
                ('actual_end', models.DateTimeField(blank=True, null=True)),
                ('contractor_name', models.CharField(blank=True, max_length=150, verbose_name='Contractor / Agency Name')),
                ('contractor_supervisor', models.CharField(blank=True, max_length=100)),
                ('workers_count', models.PositiveSmallIntegerField(default=1, verbose_name='No. of Workers')),
                ('workers_names', models.TextField(blank=True, verbose_name='Worker Names / IDs')),
                ('risk_level', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], default='medium', max_length=10)),
                ('hazards', models.TextField(blank=True, verbose_name='Identified Hazards')),
                ('precautions', models.TextField(blank=True, verbose_name='Safety Precautions / Controls')),
                ('ppe_required', models.TextField(blank=True, verbose_name='PPE Required')),
                ('emergency_procedure', models.TextField(blank=True, verbose_name='Emergency Procedure')),
                ('gas_test_required', models.BooleanField(default=False)),
                ('gas_test_result', models.CharField(blank=True, max_length=100)),
                ('isolation_required', models.BooleanField(default=False)),
                ('isolation_details', models.TextField(blank=True)),
                ('checklist_data', models.JSONField(blank=True, default=dict, verbose_name='Safety Checklist (ISO)')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('pending', 'Pending Approval'), ('approved', 'Approved / Active'), ('rejected', 'Rejected'), ('suspended', 'Suspended'), ('closed', 'Closed / Completed'), ('expired', 'Expired')], default='draft', max_length=15)),
                ('hod_approved_at', models.DateTimeField(blank=True, null=True)),
                ('hod_remarks', models.TextField(blank=True)),
                ('safety_approved_at', models.DateTimeField(blank=True, null=True)),
                ('safety_remarks', models.TextField(blank=True)),
                ('final_approved_at', models.DateTimeField(blank=True, null=True)),
                ('final_remarks', models.TextField(blank=True)),
                ('rejection_reason', models.TextField(blank=True)),
                ('suspension_reason', models.TextField(blank=True)),
                ('closure_remarks', models.TextField(blank=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='work_permits/', verbose_name='Supporting Document / Drawing')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permits_requested', to=settings.AUTH_USER_MODEL)),
                ('hod_approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='permits_hod_approved', to=settings.AUTH_USER_MODEL)),
                ('safety_approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='permits_safety_approved', to=settings.AUTH_USER_MODEL)),
                ('final_approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='permits_final_approved', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at'], 'verbose_name': 'Work Permit'},
        ),
        migrations.CreateModel(
            name='PermitComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('permit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='work_permit.workpermit')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['created_at']},
        ),
        migrations.CreateModel(
            name='PermitExtension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_end_datetime', models.DateTimeField()),
                ('reason', models.TextField()),
                ('approved', models.BooleanField(blank=True, null=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('permit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extensions', to='work_permit.workpermit')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permit_extensions', to=settings.AUTH_USER_MODEL)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='permit_extensions_approved', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
