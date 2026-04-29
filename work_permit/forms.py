from django import forms
from .models import WorkPermit, PermitComment, PermitExtension, CHECKLIST_TEMPLATES


class WorkPermitForm(forms.ModelForm):
    class Meta:
        model = WorkPermit
        fields = [
            'permit_type', 'title', 'location', 'equipment_tag', 'plant_area',
            'start_datetime', 'shift', 'renewal_required',
            'contractor_name', 'contractor_supervisor', 'workers_count', 'workers_names',
            'risk_level', 'hazards', 'precautions', 'ppe_required', 'emergency_procedure',
            'gas_test_required', 'gas_test_result', 'isolation_required', 'isolation_details',
            'moc_required', 'moc_details',
            'attachment',
        ]
        widgets = {
            'permit_type':    forms.Select(attrs={'class': 'form-select', 'id': 'id_permit_type'}),
            'title':          forms.TextInput(attrs={'class': 'form-control'}),
            'location':       forms.TextInput(attrs={'class': 'form-control'}),
            'equipment_tag':  forms.TextInput(attrs={'class': 'form-control'}),
            'plant_area':     forms.TextInput(attrs={'class': 'form-control'}),
            'start_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'shift':          forms.Select(attrs={'class': 'form-select'}),
            'contractor_name':       forms.TextInput(attrs={'class': 'form-control'}),
            'contractor_supervisor': forms.TextInput(attrs={'class': 'form-control'}),
            'workers_count':  forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'workers_names':  forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'risk_level':     forms.Select(attrs={'class': 'form-select'}),
            'hazards':        forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precautions':    forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ppe_required':   forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'emergency_procedure': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'gas_test_result':     forms.TextInput(attrs={'class': 'form-control'}),
            'isolation_details':   forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'moc_details':         forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the Management of Change details...'}),
            'attachment':     forms.FileInput(attrs={'class': 'form-control'}),
        }


class PermitApprovalForm(forms.Form):
    action  = forms.ChoiceField(choices=[('approve', 'Approve'), ('reject', 'Reject'), ('suspend', 'Suspend')])
    remarks = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)


class PermitCloseForm(forms.Form):
    closure_remarks = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False, label='Closure Remarks'
    )


class PermitCommentForm(forms.ModelForm):
    class Meta:
        model = PermitComment
        fields = ['comment']
        widgets = {'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment...'})}


class PermitExtensionForm(forms.ModelForm):
    class Meta:
        model = PermitExtension
        fields = ['new_end_datetime', 'reason']
        widgets = {
            'new_end_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
