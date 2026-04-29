from django.db import models
from django.conf import settings
from django.utils import timezone

PERMIT_TYPE_CHOICES = [
    ('hot_work',        'Hot Work Permit'),
    ('cold_work',       'Cold Work Permit'),
    ('height_work',     'Work at Height Permit'),
    ('confined_space',  'Confined Space Entry Permit'),
    ('electrical',      'Electrical Isolation Permit'),
    ('excavation',      'Excavation / Digging Permit'),
    ('radiography',     'Radiography / X-Ray Permit'),
    ('chemical',        'Chemical Handling Permit'),
    ('crane_lifting',   'Crane & Lifting Operations Permit'),
    ('demolition',      'Demolition Permit'),
    ('pressure_test',   'Pressure Testing Permit'),
    ('vehicle_entry',   'Vehicle Entry Permit'),
]

PERMIT_TYPE_COLORS = {
    'hot_work':       '#dc2626',
    'cold_work':      '#2563eb',
    'height_work':    '#d97706',
    'confined_space': '#7c3aed',
    'electrical':     '#f59e0b',
    'excavation':     '#92400e',
    'radiography':    '#be185d',
    'chemical':       '#065f46',
    'crane_lifting':  '#1e40af',
    'demolition':     '#991b1b',
    'pressure_test':  '#0e7490',
    'vehicle_entry':  '#374151',
}

PERMIT_TYPE_ICONS = {
    'hot_work':       'bi-fire',
    'cold_work':      'bi-snow',
    'height_work':    'bi-ladder',
    'confined_space': 'bi-circle-square',
    'electrical':     'bi-lightning-charge-fill',
    'excavation':     'bi-tools',
    'radiography':    'bi-radioactive',
    'chemical':       'bi-droplet-fill',
    'crane_lifting':  'bi-arrow-up-square-fill',
    'demolition':     'bi-building-x',
    'pressure_test':  'bi-speedometer2',
    'vehicle_entry':  'bi-truck-front-fill',
}

RISK_LEVEL_CHOICES = [
    ('low',      'Low'),
    ('medium',   'Medium'),
    ('high',     'High'),
    ('critical', 'Critical'),
]

STATUS_CHOICES = [
    ('draft',     'Draft'),
    ('pending',   'Pending Approval'),
    ('approved',  'Approved / Active'),
    ('rejected',  'Rejected'),
    ('suspended', 'Suspended'),
    ('closed',    'Closed / Completed'),
    ('expired',   'Expired'),
]

SHIFT_CHOICES = [
    ('A', 'A Shift (06:00–14:00)'),
    ('B', 'B Shift (14:00–22:00)'),
    ('C', 'C Shift (22:00–06:00)'),
    ('G', 'General Shift (08:00–17:00)'),
]

# ── ISO 45001 / Cement Industry Checklist Templates ───────────────────────────
CHECKLIST_TEMPLATES = {
    'hot_work': [
        {'key': 'fire_extinguisher',    'label': 'Fire extinguisher available & charged at work site'},
        {'key': 'flammables_removed',   'label': 'Flammable / combustible materials removed or shielded'},
        {'key': 'hot_work_area_clear',  'label': 'Work area cleared of dust, debris & combustibles (6 m radius)'},
        {'key': 'fire_watch',           'label': 'Fire watch person designated & briefed'},
        {'key': 'welding_screen',       'label': 'Welding screens / flash guards in place'},
        {'key': 'gas_cylinders_secure', 'label': 'Gas cylinders secured upright & stored safely'},
        {'key': 'ppe_hot',              'label': 'PPE: welding shield, leather gloves, apron, safety boots worn'},
        {'key': 'ventilation',          'label': 'Adequate ventilation / fume extraction provided'},
        {'key': 'hot_surface_marked',   'label': 'Hot surfaces marked & barricaded after work'},
        {'key': 'post_work_inspection', 'label': 'Post-work fire inspection completed (30 min after)'},
    ],
    'cold_work': [
        {'key': 'loto_applied',         'label': 'LOTO (Lock-Out / Tag-Out) applied on all energy sources'},
        {'key': 'zero_energy_verified', 'label': 'Zero energy state verified before work start'},
        {'key': 'tools_inspected',      'label': 'Hand tools & power tools inspected & in good condition'},
        {'key': 'ppe_cold',             'label': 'PPE: safety helmet, gloves, safety boots, goggles worn'},
        {'key': 'area_barricaded',      'label': 'Work area barricaded & warning signs posted'},
        {'key': 'housekeeping',         'label': 'Housekeeping maintained throughout work'},
    ],
    'height_work': [
        {'key': 'scaffold_inspected',   'label': 'Scaffold / platform inspected & tagged (green tag)'},
        {'key': 'harness_inspected',    'label': 'Full-body harness & lanyard inspected (no damage)'},
        {'key': 'anchor_point',         'label': 'Anchor point load-rated ≥ 15 kN identified & used'},
        {'key': 'edge_protection',      'label': 'Edge protection / guard rails installed'},
        {'key': 'tool_tethering',       'label': 'All tools tethered to prevent dropped objects'},
        {'key': 'exclusion_zone',       'label': 'Exclusion zone below work area barricaded'},
        {'key': 'rescue_plan',          'label': 'Rescue plan & equipment available on site'},
        {'key': 'weather_check',        'label': 'Weather conditions checked (no work in high wind / rain)'},
        {'key': 'ppe_height',           'label': 'PPE: helmet, harness, non-slip boots, hi-vis vest worn'},
    ],
    'confined_space': [
        {'key': 'atm_test_o2',          'label': 'Atmospheric test: O₂ 19.5–23.5 % (result recorded)'},
        {'key': 'atm_test_lel',         'label': 'Atmospheric test: LEL < 10 % (result recorded)'},
        {'key': 'atm_test_h2s',         'label': 'Atmospheric test: H₂S < 10 ppm (result recorded)'},
        {'key': 'co_test',              'label': 'Atmospheric test: CO < 25 ppm (result recorded)'},
        {'key': 'continuous_monitor',   'label': 'Continuous gas monitoring during work'},
        {'key': 'ventilation_cs',       'label': 'Forced ventilation (blower) running before & during entry'},
        {'key': 'standby_person',       'label': 'Trained standby / attendant stationed outside'},
        {'key': 'rescue_equipment',     'label': 'Rescue equipment (tripod, lifeline, SCBA) ready at entry'},
        {'key': 'loto_cs',              'label': 'All inlets, outlets & energy sources isolated (LOTO)'},
        {'key': 'communication',        'label': 'Communication system (radio / signal) established'},
        {'key': 'ppe_cs',               'label': 'PPE: SCBA / airline respirator, harness, lifeline worn'},
        {'key': 'entry_log',            'label': 'Entry / exit log maintained at entry point'},
    ],
    'electrical': [
        {'key': 'loto_elec',            'label': 'LOTO applied on all electrical isolation points'},
        {'key': 'voltage_verified',     'label': 'Voltage verified zero with calibrated tester'},
        {'key': 'earthing_applied',     'label': 'Earthing / grounding applied on conductors'},
        {'key': 'danger_tags',          'label': '"DANGER – DO NOT OPERATE" tags affixed on all switches'},
        {'key': 'insulated_tools',      'label': 'Insulated tools (1000 V rated) used'},
        {'key': 'ppe_elec',             'label': 'PPE: arc-flash suit, insulated gloves, face shield worn'},
        {'key': 'arc_flash_assessment', 'label': 'Arc flash hazard assessment completed'},
        {'key': 'second_person',        'label': 'Second qualified electrician present for HV work'},
        {'key': 'panel_barricaded',     'label': 'Live panels / switchgear barricaded & signed'},
    ],
    'excavation': [
        {'key': 'underground_survey',   'label': 'Underground utilities (cable, pipe) surveyed & marked'},
        {'key': 'shoring',              'label': 'Shoring / sloping / benching provided for depth > 1.2 m'},
        {'key': 'edge_protection_exc',  'label': 'Edge protection / barriers installed (1 m from edge)'},
        {'key': 'access_egress',        'label': 'Safe access / egress (ladder) provided'},
        {'key': 'spoil_placement',      'label': 'Excavated spoil placed ≥ 1 m from edge'},
        {'key': 'water_control',        'label': 'Water ingress / dewatering plan in place'},
        {'key': 'daily_inspection',     'label': 'Daily inspection of excavation walls before entry'},
        {'key': 'ppe_exc',              'label': 'PPE: helmet, safety boots, hi-vis vest, gloves worn'},
    ],
    'radiography': [
        {'key': 'radiation_survey',     'label': 'Radiation survey meter calibrated & available'},
        {'key': 'exclusion_zone_rad',   'label': 'Exclusion zone established & barricaded (rope + signs)'},
        {'key': 'dosimeter',            'label': 'Personal dosimeters issued to all workers'},
        {'key': 'rso_approval',         'label': 'Radiation Safety Officer (RSO) approval obtained'},
        {'key': 'source_secured',       'label': 'Radioactive source secured in shielded container when idle'},
        {'key': 'emergency_plan_rad',   'label': 'Emergency plan for source loss / overexposure in place'},
        {'key': 'ppe_rad',              'label': 'PPE: lead apron, thyroid shield, dosimeter worn'},
        {'key': 'night_work_lights',    'label': 'Adequate lighting for night radiography work'},
    ],
    'chemical': [
        {'key': 'sds_available',        'label': 'Safety Data Sheet (SDS / MSDS) available at work site'},
        {'key': 'chemical_labeled',     'label': 'All chemical containers properly labeled (GHS)'},
        {'key': 'spill_kit',            'label': 'Spill kit & neutralizing agent available'},
        {'key': 'eyewash_station',      'label': 'Eyewash station & emergency shower accessible'},
        {'key': 'ventilation_chem',     'label': 'Adequate ventilation / LEV provided'},
        {'key': 'incompatibles_sep',    'label': 'Incompatible chemicals stored separately'},
        {'key': 'ppe_chem',             'label': 'PPE: chemical-resistant gloves, goggles, apron, respirator worn'},
        {'key': 'disposal_plan',        'label': 'Chemical waste disposal plan in place'},
    ],
    'crane_lifting': [
        {'key': 'lift_plan',            'label': 'Lifting plan / rigging study prepared & approved'},
        {'key': 'crane_inspected',      'label': 'Crane / hoist inspected & valid third-party certificate'},
        {'key': 'slinging_inspected',   'label': 'Slings, shackles & rigging gear inspected (no damage)'},
        {'key': 'swl_verified',         'label': 'SWL of crane & rigging verified ≥ load weight'},
        {'key': 'exclusion_zone_crane', 'label': 'Exclusion zone under load established & enforced'},
        {'key': 'signal_person',        'label': 'Trained signal person / banksman designated'},
        {'key': 'overhead_lines',       'label': 'Overhead power lines identified & safe clearance maintained'},
        {'key': 'ground_bearing',       'label': 'Ground bearing capacity verified for crane outriggers'},
        {'key': 'ppe_crane',            'label': 'PPE: helmet, hi-vis vest, safety boots, gloves worn'},
        {'key': 'wind_speed',           'label': 'Wind speed checked (no lift if > 45 km/h)'},
    ],
    'demolition': [
        {'key': 'structural_survey',    'label': 'Structural survey by competent engineer completed'},
        {'key': 'utilities_isolated',   'label': 'All utilities (electric, gas, water) isolated & capped'},
        {'key': 'asbestos_survey',      'label': 'Asbestos / hazardous material survey completed'},
        {'key': 'exclusion_zone_dem',   'label': 'Exclusion zone established around demolition area'},
        {'key': 'dust_control',         'label': 'Dust suppression (water spray) in place'},
        {'key': 'debris_management',    'label': 'Debris removal & disposal plan approved'},
        {'key': 'adjacent_structures',  'label': 'Adjacent structures / equipment protected'},
        {'key': 'ppe_dem',              'label': 'PPE: helmet, dust mask (P3), goggles, gloves, boots worn'},
    ],
    'pressure_test': [
        {'key': 'test_procedure',       'label': 'Pressure test procedure / drawing approved'},
        {'key': 'gauge_calibrated',     'label': 'Pressure gauge calibrated & within range'},
        {'key': 'relief_valve',         'label': 'Relief / safety valve set at 1.1× test pressure'},
        {'key': 'exclusion_zone_pt',    'label': 'Exclusion zone established during pressurization'},
        {'key': 'visual_inspection',    'label': 'Visual inspection of all joints / welds before test'},
        {'key': 'bleed_valve',          'label': 'Bleed / vent valve available for safe depressurization'},
        {'key': 'ppe_pt',               'label': 'PPE: face shield, gloves, safety boots worn'},
        {'key': 'hold_time',            'label': 'Hold time & acceptance criteria defined in procedure'},
    ],
    'vehicle_entry': [
        {'key': 'vehicle_inspected',    'label': 'Vehicle pre-entry inspection completed (brakes, lights, horn)'},
        {'key': 'driver_briefed',       'label': 'Driver briefed on plant speed limits & traffic rules'},
        {'key': 'escort_assigned',      'label': 'Escort / banksman assigned for restricted areas'},
        {'key': 'pedestrian_clear',     'label': 'Pedestrian walkways clear & segregated'},
        {'key': 'load_secured',         'label': 'Load properly secured & within vehicle capacity'},
        {'key': 'reversing_alarm',      'label': 'Reversing alarm / camera functional'},
        {'key': 'ppe_vehicle',          'label': 'PPE: hi-vis vest, safety boots worn by all personnel'},
        {'key': 'parking_designated',   'label': 'Designated parking area used'},
    ],
}


class WorkPermit(models.Model):
    permit_number   = models.CharField(max_length=30, unique=True, editable=False)
    permit_type     = models.CharField(max_length=30, choices=PERMIT_TYPE_CHOICES)
    title           = models.CharField(max_length=200, verbose_name='Work Description / Title')

    location        = models.CharField(max_length=200, verbose_name='Work Location / Area')
    equipment_tag   = models.CharField(max_length=100, blank=True, verbose_name='Equipment / Tag No.')
    plant_area      = models.CharField(max_length=100, blank=True, verbose_name='Plant Area / Unit')
    start_datetime  = models.DateTimeField(verbose_name='Planned Start Date & Time')
    renewal_required = models.BooleanField(default=False, verbose_name='Permit Renewal Required')
    shift           = models.CharField(max_length=2, choices=SHIFT_CHOICES, blank=True)
    actual_start    = models.DateTimeField(null=True, blank=True)
    actual_end      = models.DateTimeField(null=True, blank=True)

    requested_by    = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='permits_requested'
    )
    contractor_name = models.CharField(max_length=150, blank=True, verbose_name='Contractor / Agency Name')
    contractor_supervisor = models.CharField(max_length=100, blank=True)
    workers_count   = models.PositiveSmallIntegerField(default=1, verbose_name='No. of Workers')
    workers_names   = models.TextField(blank=True, verbose_name='Worker Names / IDs')

    risk_level      = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, default='medium')
    hazards         = models.TextField(blank=True, verbose_name='Identified Hazards')
    precautions     = models.TextField(blank=True, verbose_name='Safety Precautions / Controls')
    ppe_required    = models.TextField(blank=True, verbose_name='PPE Required')
    emergency_procedure = models.TextField(blank=True, verbose_name='Emergency Procedure')
    gas_test_required   = models.BooleanField(default=False)
    gas_test_result     = models.CharField(max_length=100, blank=True)
    isolation_required  = models.BooleanField(default=False)
    isolation_details   = models.TextField(blank=True)
    moc_required        = models.BooleanField(default=False, verbose_name='MOC (Management of Change) Required')
    moc_details         = models.TextField(blank=True, verbose_name='MOC Details')

    checklist_data  = models.JSONField(default=dict, blank=True, verbose_name='Safety Checklist (ISO)')

    status          = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')

    hod_approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='permits_hod_approved'
    )
    hod_approved_at = models.DateTimeField(null=True, blank=True)
    hod_remarks     = models.TextField(blank=True)

    safety_approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='permits_safety_approved'
    )
    safety_approved_at = models.DateTimeField(null=True, blank=True)
    safety_remarks     = models.TextField(blank=True)

    final_approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='permits_final_approved'
    )
    final_approved_at = models.DateTimeField(null=True, blank=True)
    final_remarks     = models.TextField(blank=True)

    rejection_reason  = models.TextField(blank=True)
    suspension_reason = models.TextField(blank=True)
    closure_remarks   = models.TextField(blank=True)

    attachment = models.FileField(upload_to='work_permits/', blank=True, null=True,
                                  verbose_name='Supporting Document / Drawing')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Work Permit'

    def __str__(self):
        if self.workflow_type == 'renewal' and self.renewal_id:
            return f'{self.permit.permit_number} - Renewal #{self.renewal.renewal_no} Stage {self.stage + 1}: {self.stage_label}'
        return f'{self.permit_number} — {self.get_permit_type_display()}'

    @property
    def type_color(self):
        return PERMIT_TYPE_COLORS.get(self.permit_type, '#374151')

    @property
    def type_icon(self):
        return PERMIT_TYPE_ICONS.get(self.permit_type, 'bi-file-earmark-check')

    @property
    def renewal_deadline(self):
        """Midnight auto-close: 7 days if renewal_required, else same day midnight."""
        if self.actual_start:
            from datetime import time
            days = 7 if self.renewal_required else 0
            deadline_date = self.actual_start.date() + timezone.timedelta(days=days)
            return timezone.datetime.combine(deadline_date, time(23, 59, 59),
                                             tzinfo=self.actual_start.tzinfo)
        return None

    @property
    def is_expired(self):
        if self.status != 'approved':
            return False
        dl = self.renewal_deadline
        return dl is not None and timezone.now() > dl

    @property
    def is_active(self):
        if self.status != 'approved':
            return False
        dl = self.renewal_deadline
        return dl is None or timezone.now() <= dl

    @property
    def checklist_items(self):
        template = CHECKLIST_TEMPLATES.get(self.permit_type, [])
        saved = self.checklist_data or {}
        return [
            {**item, 'checked': saved.get(item['key'], False)}
            for item in template
        ]

    @property
    def checklist_score(self):
        items = self.checklist_items
        if not items:
            return None
        checked = sum(1 for i in items if i['checked'])
        return {'checked': checked, 'total': len(items), 'pct': int(checked / len(items) * 100)}

    def save(self, *args, **kwargs):
        if not self.permit_number:
            from accounts.models import SystemSetting
            setting = SystemSetting.get()
            prefix = getattr(setting, 'wp_prefix', 'WP')
            next_no = getattr(setting, 'wp_next_number', 1)
            fy = timezone.now().year % 100
            self.permit_number = f'{prefix}-{fy:02d}{(fy + 1):02d}-{next_no:05d}'
            SystemSetting.objects.filter(pk=1).update(wp_next_number=next_no + 1)
        super().save(*args, **kwargs)


import secrets


# ── Workflow Stage Definitions ────────────────────────────────────────────────
# Each stage: (label, role, dept_filter, designation_filter)
# dept_filter / designation_filter = None means no filter

def get_wp_workflow_stages(isolation_required, moc_required):
    """
    Returns ordered list of (stage_label, role, dept, designation, stage_type) tuples.
    stage_type: 'approval' | 'acknowledge'
    """
    base = [
        ('Issuer — Department HOD',           'department_hod',       None,                   None, 'approval'),
        ('Custodian — Process & Production',   'employee',             'Process & Production', None, 'approval'),
    ]
    if isolation_required:
        base += [
            ('Isolator — Electrical',          'employee',             'Electrical',           None, 'approval'),
            ('Issuer — Electrical HOD',        'department_hod',       'Electrical',           None, 'approval'),
        ]
    base.append(
        ('Safety Officer — HSEF',              'hsef_safety',          'HSEF',                 'Safety Officer', 'approval')
    )
    if moc_required:
        base.append(
            ('MOC — President / Plant Head',   'president_plant_head', None,                   None, 'approval')
        )
    return base


def get_wp_renewal_workflow_stages():
    """
    Renewal workflow: Issuer (acknowledge) → Custodian (approval) → Safety Officer (acknowledge).
    stage_type: 'approval' | 'acknowledge'
    """
    return [
        ('Renewal — Issuer (Department HOD)',        'department_hod',  None,   None,             'acknowledge'),
        ('Renewal — Custodian (Process & Production)','employee',        'Process & Production', None, 'approval'),
        ('Renewal — Safety Officer (HSEF)',          'hsef_safety',     'HSEF', 'Safety Officer', 'acknowledge'),
    ]


STAGE_STATUS_CHOICES = [
    ('pending',  'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]


class PermitComment(models.Model):
    permit     = models.ForeignKey(WorkPermit, on_delete=models.CASCADE, related_name='comments')
    author     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username} on {self.permit.permit_number}'


class PermitExtension(models.Model):
    permit           = models.ForeignKey(WorkPermit, on_delete=models.CASCADE, related_name='extensions')
    requested_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         related_name='permit_extensions')
    new_end_datetime = models.DateTimeField()
    reason           = models.TextField()
    approved         = models.BooleanField(null=True, blank=True)
    approved_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='permit_extensions_approved')
    approved_at      = models.DateTimeField(null=True, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Extension for {self.permit.permit_number}'


class PermitRenewal(models.Model):
    """Tracks each renewal cycle for a WorkPermit."""
    permit       = models.ForeignKey(WorkPermit, on_delete=models.CASCADE, related_name='renewals')
    renewal_no   = models.PositiveSmallIntegerField()          # 1, 2, 3 ...
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='permit_renewals_requested'
    )
    requested_at  = models.DateTimeField(auto_now_add=True)
    approved_at   = models.DateTimeField(null=True, blank=True)  # set when renewal workflow completes
    valid_from    = models.DateTimeField(null=True, blank=True)
    valid_until   = models.DateTimeField(null=True, blank=True)  # midnight day 7
    status        = models.CharField(max_length=20, default='pending')  # pending | approved | rejected

    class Meta:
        ordering = ['renewal_no']

    def __str__(self):
        return f'{self.permit.permit_number} — Renewal #{self.renewal_no}'


class PermitApprovalStage(models.Model):
    """Tracks each approval stage in the WP workflow."""
    permit        = models.ForeignKey(WorkPermit, on_delete=models.CASCADE, related_name='approval_stages')
    renewal       = models.ForeignKey(
        PermitRenewal, null=True, blank=True,
        on_delete=models.CASCADE, related_name='approval_stages'
    )
    workflow_type = models.CharField(max_length=20, default='main')  # main | renewal
    stage         = models.PositiveSmallIntegerField()        # 0-based index
    stage_label   = models.CharField(max_length=120)          # e.g. 'Issuer — Department HOD'
    approver_role = models.CharField(max_length=30)           # role expected
    approver_dept = models.CharField(max_length=100, blank=True)  # optional dept filter
    approver_desig= models.CharField(max_length=100, blank=True)  # optional designation filter
    approver      = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='wp_stage_approvals'
    )
    status        = models.CharField(max_length=20, choices=STAGE_STATUS_CHOICES, default='pending')
    stage_type    = models.CharField(max_length=20, default='approval')  # 'approval' | 'acknowledge'
    remarks       = models.TextField(blank=True)
    token         = models.CharField(max_length=64, blank=True, null=True, unique=True)
    acted_at      = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['stage']
        unique_together = ('permit', 'workflow_type', 'renewal', 'stage')

    def __str__(self):
        return f'{self.permit.permit_number} — Stage {self.stage + 1}: {self.stage_label}'
