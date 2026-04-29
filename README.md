
"# ERP-System" 

# ERP System — Blueprint
**Organization:** Cement Industry | **Standard:** ISO 45001:2018  
**Stack:** Django 4.2.7 · Python 3.13 · MySQL · Bootstrap 5
**Last Updated:** 2025  
**Server:** LAN — `Your Hosting IP`

---

## 1. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER                           │
│              Bootstrap 5 · HTML · CSS · JS                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP / LAN
┌──────────────────────────▼──────────────────────────────────────┐
│                    DJANGO APPLICATION                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ accounts │  │dashboard │  │ internal │  │   visitor    │   │
│  │  (auth)  │  │  (home)  │  │   _pass  │  │    _pass     │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │material  │  │helpdesk  │  │grievance │  │ work_permit  │   │
│  │  _pass   │  │   (HD)   │  │  (GRV)   │  │   (PTW)      │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
│                                                                 │
│  Middleware: Maintenance · SingleLogin · Inauguration           │
│  Email: SMTP (Gmail) · Token-based approval links               │
│  Backup: Daily JSON · Windows Task Scheduler                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │ Django ORM
┌──────────────────────────▼──────────────────────────────────────┐
│                    MySQL DATABASE                               │
│                    gate_pass_db · utf8mb4                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Module Map

| # | Module | URL Prefix | App | Key Purpose |
|---|--------|-----------|-----|-------------|
| 1 | Dashboard | `/` | `dashboard` | Summary stats, charts, recent activity |
| 2 | Accounts | `/accounts/` | `accounts` | Users, roles, permissions, settings |
| 3 | Internal Gate Pass | `/internal-pass/` | `internal_pass` | Employee movement approvals (IGP) |
| 4 | Visitor Gate Pass | `/visitor-pass/` | `visitor_pass` | Visitor entry management (VGP) |
| 5 | Material Gate Pass | `/material-pass/` | `material_pass` | Material movement + requests (MGP/MR) |
| 6 | IT Help Desk | `/helpdesk/` | `helpdesk` | IT ticket management (HD) |
| 7 | Grievance | `/grievance/` | `grievance` | Employee grievance redressal (GRV) |
| 8 | Work Permit | `/work-permit/` | `work_permit` | Permit to Work system (PTW) |

---

## 3. Role & Permission Matrix

### 3.1 Roles (Hierarchy — High to Low)
```
administrator          → Full access, bypasses nothing (goes through workflow)
management             → Full visibility, approval rights
president_plant_head   → MOC approvals, full visibility
department_hod         → Department-level approvals
hr                     → HR-related access
security               → Gate pass checkout/entry
employee               → Standard user, raises requests
```

### 3.2 Granular Permission Flags (per Employee)
| Module | Flags |
|--------|-------|
| Dashboard | `perm_dashboard_view` |
| Accounts | `perm_accounts_view/write/delete/export` |
| IGP | `perm_igp_view/write/delete/approve/bypass/export` |
| VGP | `perm_vgp_view/write/delete/approve/bypass/export` |
| MGP | `perm_mgp_view/write/delete/approve/export/request` |
| Help Desk | `perm_helpdesk_view/write/manage` |
| Grievance | `perm_grv_view/write/manage` |
| Work Permit | `perm_wp_view/write/approve/delete/report` |
| Reports | `perm_reports_igp/vgp/mgp/grv/audit` |

> Each employee can have **one primary role + additional roles** and **one primary department + additional departments**.

---

## 4. Module Details

### 4.1 Internal Gate Pass (IGP)

**Purpose:** Track employee outings/movements with multi-stage approval.

**Workflow (4 variants based on creator role):**
```
Workflow 1 — Employee:
  Creator → Dept HOD → HR → Security (3 stages)

Workflow 2 — Department HOD:
  Creator → President/Plant Head → HR → Security (3 stages)

Workflow 3 — HR:
  Creator → President/Plant Head → Security (2 stages)

Workflow 4 — President/Plant Head:
  Creator → Management → Security (2 stages)

Bypass Roles (Direct Approval):
  Management, Administrator, Security → No workflow stages (0 stages)
```

**Status Flow:** `pending → in_progress → approved → returned`  
**Rejection:** Any stage can reject → status = `rejected`  
**Key Models:** `InternalGatePass`, `GatePassApproval`  
**Email:** Token-based approve/reject links sent to each stage approver  
**Print:** Pass print layout  
**Reports:** Excel + PDF export  

**Button Visibility Rules:**
- **Edit Button:** Hidden for `rejected` and `returned` passes
- **Approve/Reject Button:** Hidden for `returned` passes (automatically handled by workflow logic)
- **Mark Returned Button:** Only visible for `approved` passes
- **Completion Status:** Shows success alert with actual return time for `returned` passes  

---

### 4.2 Visitor Gate Pass (VGP)

**Purpose:** Manage visitor entry, approval, photo capture, and checkout.

**Workflow:**
```
Creator → Contact Person (approval) → Entry → Checkout
```

**Status Flow:** `pending → approved → checked_out` / `rejected`  
**Key Models:** `VisitorGatePass`  
**Features:** Photo capture/upload, access card tracking, vehicle number  
**Email:** Token-based approval link to contact person  
**Print:** Visitor pass print  
**Reports:** Excel + PDF export  

---

### 4.3 Material Gate Pass (MGP) + Material Request (MR)

**Purpose:** Control material movement in/out of plant with optional request workflow.

**MR → MGP Workflow:**
```
Employee creates MR → Dept HOD approval → Store HOD approval → Store converts to MGP → MGP approved
```

**Direct MGP Workflow:**
```
Store creates MGP → Store HOD approves
```

**Status Flow (MR):** `submitted → hod_approved → store_approved → converted`  
**Status Flow (MGP):** `pending → approved → returned`  
**Key Models:** `MaterialRequest`, `MaterialRequestItem`, `MaterialGatePass`, `MaterialItem`, `MaterialAttachment`  
**Print:** 3-copy challan (Original / Duplicate / Triplicate)  
**Reports:** Excel + PDF export  

---

### 4.4 IT Help Desk (HD)

**Purpose:** Internal IT support ticket management.

**Workflow:**
```
Employee raises ticket → IT assigns → IT resolves → Requester notified
```

**Status Flow:** `open → in_progress → resolved → closed`  
**Key Models:** `Ticket`, `TicketComment`  
**Visibility:** IT dept sees all; others see own dept tickets  
**Reports:** Ticket stats  

---

### 4.5 Grievance Redressal (GRV)

**Purpose:** Employee grievance submission and management resolution.

**Workflow:**
```
Employee raises grievance → Management notified → HOD/HR notified → Resolution
```

**Status Flow:** `submitted → under_review → resolved → closed`  
**Key Models:** `Grievance`, `GrievanceComment`  
**Reports:** Excel + PDF export  

---

### 4.6 Work Permit / Permit to Work (PTW)

**Purpose:** ISO 45001:2018 compliant safety permit system for hazardous work.

**Permit Types (12):**
```
Hot Work · Cold Work · Work at Height · Confined Space Entry
Electrical Isolation · Excavation · Radiography · Chemical Handling
Crane & Lifting · Demolition · Pressure Testing · Vehicle Entry
```

**Risk Levels:** `Low → Medium → High → Critical`

**Key Fields:**
| Field | Description |
|-------|-------------|
| `permit_number` | Auto-generated (prefix + FY + sequence) — never changes on renewal |
| `renewal_required` | If checked: permit valid 7 days from approval, then auto-closes at midnight. If unchecked: auto-closes at midnight of approval day |
| `moc_required` + `moc_details` | MOC checkbox + free-text details (shown on print) |
| `isolation_required` + `isolation_details` | Adds 2 extra stages to workflow |
| `actual_start` | Set automatically when permit reaches fully approved status |

**Permit Validity & Auto-Close:**
```
renewal_required = False  →  Auto-closes at midnight of approval day
renewal_required = True   →  Auto-closes at midnight of day 7 from approval
```
> Auto-close sets status = `closed`. Only **Administrator** can re-open.

---

**Main Workflow Variants (determined by Isolation + MOC checkboxes):**

All stages are `approval` type — approver must act via email link or portal.

```
Standard (No Isolation, No MOC) — 4 stages:
  Issuer (Dept HOD) → Custodian (Process & Production)
  → Safety Officer (HSEF) → [Co-Permit: manual sign on print only]

Isolation Checked — 6 stages:
  Issuer (Dept HOD) → Custodian (Process & Production)
  → Isolator (Electrical) → Issuer (Electrical HOD)
  → Safety Officer (HSEF) → [Co-Permit: manual sign on print only]

Isolation + MOC — 7 stages:
  Issuer (Dept HOD) → Custodian (Process & Production)
  → Isolator (Electrical) → Issuer (Electrical HOD)
  → Safety Officer (HSEF) → MOC (President/Plant Head)
  → [Co-Permit: manual sign on print only]

MOC Only — 5 stages:
  Issuer (Dept HOD) → Custodian (Process & Production)
  → Safety Officer (HSEF) → MOC (President/Plant Head)
  → [Co-Permit: manual sign on print only]
```

> **Co-Permit** is always a blank manual signature box on the printed PTW form only — it is NOT a workflow stage and requires no system action.

---

**Renewal Workflow (triggered when initiator clicks "Request Renewal" on a closed permit):**

Only available when `renewal_required = True` and permit status = `closed`.  
Document number never changes. A fresh 7-day validity clock starts from re-approval.

```
Stage 1 — Issuer (Dept HOD)         [ACKNOWLEDGE — email sent, auto-marked done]
Stage 2 — Custodian (Process & Prod) [APPROVAL    — must approve via email/portal]
Stage 3 — Safety Officer (HSEF)      [ACKNOWLEDGE — email sent, auto-marked done]
```

> Acknowledge stages: email is sent for awareness, stage is auto-approved immediately.  
> Approval stage: workflow pauses until Custodian acts.  
> On completion: permit status → `approved`, new `actual_start` set, 7-day clock restarts.

---

**Stage Approver Rules:**
| Stage | Role Required | Dept Filter | Designation Filter |
|-------|--------------|-------------|-------------------|
| Issuer (HOD) | `department_hod` | Initiator's dept | — |
| Custodian | `employee` | Process & Production | — |
| Isolator | `employee` | Electrical | — |
| Electrical HOD | `department_hod` | Electrical | — |
| Safety Officer | `hsef_safety` | HSEF | Safety Officer |
| MOC | `president_plant_head` | — | — |

**Stage Types:**
| Type | Behaviour |
|------|-----------|
| `approval` | Workflow pauses; approver must Approve or Reject via email/portal |
| `acknowledge` | Email sent for awareness; stage auto-approved immediately; workflow continues |

**Status Flow:**
```
draft → pending → approved → closed (auto at midnight or manual)
                ↘ rejected
                ↘ suspended
```
> `closed` permits with `renewal_required=True` can be renewed by initiator.  
> Only Administrator can re-open a `closed` permit directly (bypasses workflow).

**Key Models:**
| Model | Purpose |
|-------|---------|
| `WorkPermit` | Main permit record |
| `PermitApprovalStage` | Each workflow stage (includes `stage_type`: approval/acknowledge, `workflow_type`: main/renewal) |
| `PermitRenewal` | Tracks each renewal cycle (renewal_no, status, valid_from, valid_until) |
| `PermitComment` | Comments on permit |

**Email:** HTML email with Approve/Reject buttons (approval stages) or single Acknowledge button (acknowledge stages) + workflow progress bar  
**Print:** A4 PTW form — dynamic approval grid (one column per stage) + Co-Permit blank signature box always appended  
**Reports:** Excel + PDF (Summary & Detail views)  
**ISO 45001 Checklist:** Per-permit-type checklist loaded dynamically via API; "✓ Check All" button checks all items at once; score badge shows `checked/total (%)`  

---

## 5. Database Schema (Key Relationships)

```
Employee ──────────────────────────────────────────────────────────┐
  │                                                                │
  ├──< InternalGatePass >──< GatePassApproval                     │
  │                                                                │
  ├──< VisitorGatePass                                             │
  │                                                                │
  ├──< MaterialRequest >──< MaterialRequestItem                   │
  │         │                                                      │
  │         └──converts──> MaterialGatePass >──< MaterialItem     │
  │                                       └──< MaterialAttachment │
  │                                                                │
  ├──< Ticket >──< TicketComment                                  │
  │                                                                │
  ├──< Grievance >──< GrievanceComment                            │
  │                                                                │
  └──< WorkPermit >──< PermitApprovalStage (stage_type, workflow_type) │
              ├──< PermitRenewal                                    │
              └──< PermitComment                                    │
                                                                   │
SystemSetting (singleton pk=1) ────────────────────────────────────┘
  Series prefixes · SMTP · Session · Maintenance · Notification channels
```

---

## 6. Notification & Email System

```
Action Triggered
      │
      ▼
SystemSetting.notif_[module]_email == True?
      │ Yes                    │ No
      ▼                        ▼
Send HTML Email            Skip email
(SMTP via Gmail)
      │
      ▼
EmailLog (audit trail)

SystemSetting.notif_[module]_popup == True?
      │ Yes
      ▼
Notification record created → shown in bell icon
```

**Email Types:**
- Stage approval request (Approve/Reject buttons + progress bar) — approval stages
- Stage acknowledgement (Acknowledge button only) — acknowledge stages
- Final approval / rejection notification to initiator (with full approval trail)
- Forgot password reset link
- Admin OTP login code

---

## 7. Security & Session

| Feature | Detail |
|---------|--------|
| Authentication | Custom `Employee` model (`AUTH_USER_MODEL`) |
| Admin OTP | 6-digit OTP emailed on admin login, expires in 5 min |
| Single Login | One active session per user; duplicate session kicked |
| Session Timeout | Configurable (default 20 min inactivity) |
| Password Policy | Must change on first login |
| Forgot Password | Token-based email reset link |
| CSRF | Django CSRF middleware on all POST forms |
| Maintenance Mode | Middleware blocks all non-admin access |

---

## 8. System Settings (Admin Panel)

Accessible at `/accounts/settings/` — Administrator only.

| Section | Controls |
|---------|----------|
| Pass Series | Prefix + next number for IGP/VGP/MGP/MR/GRV/WP |
| Work Permit | WP prefix, Doc Ref, Revision number |
| SMTP | Host, port, TLS, user, password, from address |
| Session | Inactivity timeout (minutes) |
| Maintenance | Enable/disable + custom message |
| Inauguration | Welcome page enable/version/messages |
| Workflow Notifications | Popup/email toggles per module |
| Role Templates | Default permission sets per role |
| Module Access | Which modules visible per role |
| WP Workflow | Visual diagram of all 5 workflow variants (Standard / Isolation / Isolation+MOC / MOC Only / **Renewal**) |
| Email Recipients | Which roles receive emails per module |
| Print Format | Field visibility on printed passes |
| Database Reset | Delete all records per module + reset counter |
| Backup | Download JSON backup, restore from backup |
| Email Log | Audit trail of all sent/failed emails |
| Notification Log | Audit trail of all popup notifications |
| Audit Log | Full system action log |
| Daily Quotes | 365 daily inspiration quotes management |

---

## 9. Backup System

| Type | File | Schedule |
|------|------|----------|
| Daily Auto Backup | `DAILY_BACKUP.bat` → `manage.py auto_backup` | Windows Task Scheduler — Daily 00:00 |
| Manual Download | System Settings → Backup tab | On demand |
| Restore | System Settings → Backup tab | On demand |

**Backup includes:** Settings · Employees · IGP · VGP · MGP · MR · HD · Grievance · **Work Permit** (permits + stages + comments)  
**Retention:** Last 30 backups kept automatically  
**Location:** `Z:\erp system\backups\auto_backup_YYYYMMDD_HHMMSS.json`  
**Version:** `2.0`

---

## 10. File & Folder Structure

```
erp system/
├── accounts/               ← Auth, users, settings, notifications
│   ├── management/commands/auto_backup.py  ← Daily backup (v2.0)
│   ├── middleware.py        ← Maintenance, SingleLogin, Inauguration
│   ├── models.py            ← Employee, SystemSetting, AuditLog, Notification...
│   ├── notification_service.py
│   ├── report_utils.py      ← Shared PDF/Excel helpers
│   └── workflow_manager.py
├── dashboard/              ← Home page stats & charts
├── internal_pass/          ← IGP module
├── visitor_pass/           ← VGP module
├── material_pass/          ← MGP + MR module
├── helpdesk/               ← HD ticketing module
├── grievance/              ← GRV module
├── work_permit/            ← PTW / Work Permit module
│   └── migrations/
│       ├── 0001_initial.py
│       ├── 0002_workpermit_moc_required.py
│       ├── 0003_permitapprovalstage.py
│       ├── 0004_workpermit_moc_details.py
│       ├── 0005_remove_end_datetime_add_renewal.py
│       ├── 0006_permitapprovalstage_stage_type.py
│       ├── 0007_permitrenewal.py
│       └── 0008_permitapprovalstage_workflow_type_and_renewal.py
├── gate_pass_system/       ← Django project config (settings, urls, wsgi)
├── templates/              ← All HTML templates (per module)
├── static/                 ← CSS, JS, images (Unity Logo)
├── media/                  ← Uploaded files (visitor photos, WP attachments)
├── backups/                ← Daily JSON backups
├── DAILY_BACKUP.bat        ← Windows scheduled backup runner
├── RUN.bat                 ← Start Django dev server
├── SETUP.bat               ← First-time setup
├── requirements.txt        ← Python dependencies
└── manage.py
```

---

## 11. Tech Stack & Dependencies

| Package | Version | Purpose |
|---------|---------|---------| 
| Django | 4.2.7 | Web framework |
| PyMySQL | 1.1.1 | MySQL connector |
| cryptography | 42.0.8 | PyMySQL TLS support |
| openpyxl | 3.1.2 | Excel export |
| reportlab | 4.0.7 | PDF generation |
| django-crispy-forms | 2.1 | Form rendering |
| crispy-bootstrap5 | 0.7 | Bootstrap 5 form theme |
| Bootstrap | 5.x (CDN) | UI framework |
| Bootstrap Icons | (CDN) | Icon set |

---

## 12. URL Structure

```
/                           → Dashboard (home)
/accounts/login/            → Login
/accounts/logout/           → Logout
/accounts/employees/        → Employee list
/accounts/employees/create/ → Create employee
/accounts/settings/         → System settings (admin only)
/accounts/audit-log/        → Audit log (admin only)

/internal-pass/             → IGP dashboard
/internal-pass/list/        → IGP list
/internal-pass/<pk>/        → IGP detail
/internal-pass/stage/<token>/<action>/ → Email approval link

/visitor-pass/              → VGP list
/visitor-pass/<pk>/         → VGP detail
/visitor-pass/token/<token>/<action>/  → Email approval link

/material-pass/             → MGP list
/material-pass/request/     → MR list
/material-pass/<pk>/        → MGP detail

/helpdesk/                  → HD dashboard
/helpdesk/tickets/          → Ticket list
/helpdesk/tickets/<pk>/     → Ticket detail

/grievance/                 → GRV dashboard
/grievance/list/            → GRV list
/grievance/<pk>/            → GRV detail

/work-permit/               → WP dashboard
/work-permit/list/          → WP list
/work-permit/create/        → Create permit
/work-permit/<pk>/          → Permit detail
/work-permit/<pk>/edit/     → Edit permit (draft/rejected only)
/work-permit/<pk>/submit/   → Submit draft for approval
/work-permit/<pk>/approve/  → Approve/reject/suspend stage (portal)
/work-permit/<pk>/close/    → Close permit
/work-permit/<pk>/reopen/   → Re-open closed permit (admin only)
/work-permit/<pk>/renew/    → Start renewal workflow (initiator, renewal_required=True)
/work-permit/<pk>/print/    → Print PTW form (A4)
/work-permit/<pk>/delete/   → Delete permit (admin only)
/work-permit/stage/<token>/<action>/ → Email approval/acknowledge link
/work-permit/report/        → Reports (Summary & Detail)
/work-permit/report/export/excel/    → Excel export
/work-permit/report/export/pdf/      → PDF export
/work-permit/api/checklist-template/ → ISO checklist API
```

---

## 13. Work Permit — Change Log

| Version | Change |
|---------|--------|
| v1.0 | Initial PTW module with 4 workflow variants + Co-Permit |
| v1.1 | Added MOC details text field (shown on print) |
| v1.2 | Removed Co-Permit as workflow stage; kept as print-only manual signature box |
| v1.3 | Removed extension requests feature |
| v1.4 | Replaced `end_datetime` with `renewal_required` checkbox; midnight auto-close logic |
| v1.5 | Fixed email-based approval bug (approver not set on token action) |
| v1.6 | Added `stage_type` (approval/acknowledge) to `PermitApprovalStage` |
| v1.7 | Added Renewal Workflow: Issuer (ack) → Custodian (approval) → Safety Officer (ack) |
| v1.8 | Added Re-open (admin only) and Request Renewal (initiator) buttons on detail page |
| v1.9 | Renewal workflow shown in System Settings Workflow diagram |
| v2.0 | Added `PermitRenewal` model (tracks renewal cycles with valid_from/valid_until) |
| v2.1 | Added `workflow_type` + `renewal` FK to `PermitApprovalStage` (main vs renewal stages) |
| v2.2 | Fixed `IndentationError` in `views.py` — removed orphaned duplicate code block after `report_export_pdf` |
| v2.3 | Added "✓ Check All" button to ISO 45001 Safety Checklist on permit form |

---

## 15. IGP Module — Change Log

| Version | Change |
|---------|--------|
| v1.0 | Initial IGP module with basic workflow |
| v1.1 | Added multi-role workflow variants based on creator role |
| v1.2 | Fixed HR workflow to prevent self-approval (HR → President → Security) |
| v1.3 | Added bypass roles (Management, Administrator, Security) with direct approval |
| v1.4 | Added workflow display in form showing approval steps before submission |
| v1.5 | Fixed administrator approval button functionality for direct approval |
| v1.6 | Added button hiding for returned passes: Edit and Approve/Reject buttons hidden |
| v1.7 | Added completion status display with actual return time for returned passes |
| v1.8 | Enhanced role resolution logic to handle multi-role users correctly |

---

## 16. Deployment Checklist

- [ ] Set `DEBUG = False` in production
- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `ALLOWED_HOSTS` to actual server IP/domain
- [ ] Store SMTP password in environment variable (not in settings.py)
- [ ] Run `python manage.py collectstatic`
- [ ] Run `python manage.py migrate`
- [ ] Schedule `DAILY_BACKUP.bat` in Windows Task Scheduler (daily 00:00)
- [ ] Set `SITE_BASE_URL` to actual LAN/WAN URL for email links
- [ ] Verify MySQL `gate_pass_db` charset = `utf8mb4`
- [ ] Test SMTP from System Settings → Test Email

---

*Blueprint v2.3 — ERP System · Django 4.2.7 · Python 3.13 · MySQL*
