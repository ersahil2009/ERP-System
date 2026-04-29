from django.contrib import admin
from .models import WorkPermit, PermitComment, PermitExtension


class PermitCommentInline(admin.TabularInline):
    model = PermitComment
    extra = 0
    readonly_fields = ('author', 'created_at')


class PermitExtensionInline(admin.TabularInline):
    model = PermitExtension
    extra = 0
    readonly_fields = ('requested_by', 'created_at', 'approved_by', 'approved_at')


@admin.register(WorkPermit)
class WorkPermitAdmin(admin.ModelAdmin):
    list_display  = ('permit_number', 'permit_type', 'title', 'location', 'risk_level',
                     'status', 'requested_by', 'start_datetime', 'renewal_required', 'created_at')
    list_filter   = ('status', 'permit_type', 'risk_level', 'shift')
    search_fields = ('permit_number', 'title', 'location', 'contractor_name')
    readonly_fields = ('permit_number', 'created_at', 'updated_at')
    inlines = [PermitCommentInline, PermitExtensionInline]
    fieldsets = (
        ('Identification', {
            'fields': ('permit_number', 'permit_type', 'title', 'status')
        }),
        ('Location & Timing', {
            'fields': ('location', 'equipment_tag', 'plant_area', 'shift',
                       'start_datetime', 'renewal_required', 'actual_start', 'actual_end')
        }),
        ('Personnel', {
            'fields': ('requested_by', 'contractor_name', 'contractor_supervisor',
                       'workers_count', 'workers_names')
        }),
        ('Risk & Safety', {
            'fields': ('risk_level', 'hazards', 'precautions', 'ppe_required',
                       'emergency_procedure', 'gas_test_required', 'gas_test_result',
                       'isolation_required', 'isolation_details')
        }),
        ('ISO Checklist', {'fields': ('checklist_data',)}),
        ('Approval Workflow', {
            'fields': ('hod_approved_by', 'hod_approved_at', 'hod_remarks',
                       'safety_approved_by', 'safety_approved_at', 'safety_remarks',
                       'final_approved_by', 'final_approved_at', 'final_remarks',
                       'rejection_reason', 'suspension_reason', 'closure_remarks')
        }),
        ('Attachment', {'fields': ('attachment',)}),
        ('Audit', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(PermitComment)
class PermitCommentAdmin(admin.ModelAdmin):
    list_display = ('permit', 'author', 'comment', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(PermitExtension)
class PermitExtensionAdmin(admin.ModelAdmin):
    list_display = ('permit', 'requested_by', 'new_end_datetime', 'approved', 'approved_by')
    readonly_fields = ('created_at', 'approved_at')
