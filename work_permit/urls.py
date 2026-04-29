from django.urls import path
from . import views

app_name = 'work_permit'

urlpatterns = [
    path('',                            views.dashboard,             name='dashboard'),
    path('list/',                       views.permit_list,           name='list'),
    path('create/',                     views.permit_create,         name='create'),
    path('<int:pk>/',                   views.permit_detail,         name='detail'),
    path('<int:pk>/edit/',              views.permit_edit,           name='edit'),
    path('<int:pk>/delete/',            views.permit_delete,         name='delete'),
    path('<int:pk>/submit/',            views.permit_submit,         name='submit'),
    path('<int:pk>/approve/',           views.permit_approve,        name='approve'),
    path('<int:pk>/close/',             views.permit_close,          name='close'),
    path('<int:pk>/reopen/',            views.permit_reopen,         name='reopen'),
    path('<int:pk>/renew/',             views.permit_renew,          name='renew'),
    path('<int:pk>/print/',             views.permit_print,          name='print'),
    path('report/',                     views.permit_report,         name='report'),
    path('report/export/excel/',         views.report_export_excel,   name='report_excel'),
    path('report/export/pdf/',           views.report_export_pdf,     name='report_pdf'),
    path('extension/<int:ext_pk>/action/', views.approve_extension,  name='approve_extension'),
    path('stage/<str:token>/<str:action>/', views.wp_stage_action, name='stage_action'),
    path('api/checklist-template/',     views.checklist_template_api, name='checklist_api'),
]
