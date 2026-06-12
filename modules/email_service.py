# # modules/email_service.py
# import os
# import smtplib
# import re
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from datetime import datetime
# from typing import Optional
# from dotenv import load_dotenv

# load_dotenv()

# SMTP_EMAIL    = os.getenv("SMTP_EMAIL", "")
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
# SMTP_HOST     = "smtp.gmail.com"
# SMTP_PORT     = 587

# # ── Email Templates ────────────────────────────────────────────────────────────

# def _template_selected(candidate_name: str, role: str, company: str,
#                         recruiter_name: str, recruiter_role: str,
#                         recruiter_org: str) -> tuple[str, str]:
#     subject = f"Congratulations! You've Been Shortlisted – {role} at {company}"
#     body = f"""
# <!DOCTYPE html>
# <html>
# <body style="font-family: Arial, sans-serif; background:#f4f4f4; padding:20px;">
#   <div style="max-width:600px; margin:auto; background:white; border-radius:10px;
#               box-shadow:0 2px 8px rgba(0,0,0,0.1); overflow:hidden;">

#     <div style="background:linear-gradient(135deg,#059669,#047857); padding:28px 32px;">
#       <h1 style="color:white; margin:0; font-size:22px;">🎉 Congratulations, {candidate_name}!</h1>
#       <p style="color:#D1FAE5; margin:8px 0 0; font-size:14px;">You've been shortlisted!</p>
#     </div>

#     <div style="padding:28px 32px; color:#1F2937;">
#       <p style="font-size:15px; line-height:1.7;">
#         We are delighted to inform you that after a thorough review of your application, you have been
#         <strong style="color:#059669;">shortlisted</strong> for the position of
#         <strong>{role}</strong> at <strong>{company}</strong>.
#       </p>

#       <div style="background:#F0FDF4; border-left:4px solid #059669; padding:14px 18px;
#                   border-radius:6px; margin:20px 0;">
#         <p style="margin:0; font-size:14px; color:#065F46;">
#           <strong>Position:</strong> {role}<br>
#           <strong>Company:</strong> {company}
#         </p>
#       </div>

#       <p style="font-size:15px; line-height:1.7;">
#         Our team was impressed with your profile and experience. We will be in touch shortly with
#         details regarding the next steps in the recruitment process.
#       </p>
#       <p style="font-size:15px; line-height:1.7;">
#         Please keep an eye on your inbox and ensure your contact details are up to date.
#         If you have any questions, feel free to reach out to us directly.
#       </p>
#       <p style="font-size:15px; line-height:1.7;">We look forward to connecting with you soon!</p>

#       <hr style="border:none; border-top:1px solid #E5E7EB; margin:24px 0;">
#       <p style="font-size:14px; color:#6B7280; margin:0;">
#         Best Regards,<br>
#         <strong style="color:#1F2937;">{recruiter_name}</strong><br>
#         {recruiter_role}<br>
#         {recruiter_org}<br>
#         <em>AI Recruiter Agent</em>
#       </p>
#     </div>

#     <div style="background:#F9FAFB; padding:12px 32px; text-align:center;">
#       <p style="color:#9CA3AF; font-size:11px; margin:0;">
#         This email was sent by AI Recruiter Agent on behalf of {company}.
#       </p>
#     </div>
#   </div>
# </body>
# </html>
# """
#     return subject, body


# def _template_rejected(candidate_name: str, role: str, company: str,
#                         recruiter_name: str, recruiter_role: str,
#                         recruiter_org: str) -> tuple[str, str]:
#     subject = f"Application Update – {role} at {company}"
#     body = f"""
# <!DOCTYPE html>
# <html>
# <body style="font-family: Arial, sans-serif; background:#f4f4f4; padding:20px;">
#   <div style="max-width:600px; margin:auto; background:white; border-radius:10px;
#               box-shadow:0 2px 8px rgba(0,0,0,0.1); overflow:hidden;">

#     <div style="background:linear-gradient(135deg,#4F46E5,#7C3AED); padding:28px 32px;">
#       <h1 style="color:white; margin:0; font-size:22px;">Application Update</h1>
#       <p style="color:#C7D2FE; margin:8px 0 0; font-size:14px;">{role} at {company}</p>
#     </div>

#     <div style="padding:28px 32px; color:#1F2937;">
#       <p style="font-size:15px;">Dear {candidate_name},</p>
#       <p style="font-size:15px; line-height:1.7;">
#         Thank you for taking the time to apply for the <strong>{role}</strong> position at
#         <strong>{company}</strong> and for your interest in joining our team.
#       </p>
#       <p style="font-size:15px; line-height:1.7;">
#         After careful consideration of all applications, we regret to inform you that we will not be
#         moving forward with your application at this time. This was a highly competitive process and
#         the decision was not easy.
#       </p>
#       <p style="font-size:15px; line-height:1.7;">
#         We genuinely appreciate the effort you put into your application and encourage you to apply
#         for future openings that match your skills and experience. We will keep your profile on file
#         for upcoming opportunities.
#       </p>
#       <p style="font-size:15px; line-height:1.7;">
#         We wish you all the very best in your career journey ahead.
#       </p>

#       <hr style="border:none; border-top:1px solid #E5E7EB; margin:24px 0;">
#       <p style="font-size:14px; color:#6B7280; margin:0;">
#         Best Regards,<br>
#         <strong style="color:#1F2937;">{recruiter_name}</strong><br>
#         {recruiter_role}<br>
#         {recruiter_org}<br>
#         <em>AI Recruiter Agent</em>
#       </p>
#     </div>

#     <div style="background:#F9FAFB; padding:12px 32px; text-align:center;">
#       <p style="color:#9CA3AF; font-size:11px; margin:0;">
#         This email was sent by AI Recruiter Agent on behalf of {company}.
#       </p>
#     </div>
#   </div>
# </body>
# </html>
# """
#     return subject, body


# def _template_technical_round(candidate_name: str, role: str, company: str,
#                                recruiter_name: str, recruiter_role: str,
#                                recruiter_org: str) -> tuple[str, str]:
#     subject = f"Technical Interview Invitation – {role} at {company}"
#     body = f"""
# <!DOCTYPE html>
# <html>
# <body style="font-family: Arial, sans-serif; background:#f4f4f4; padding:20px;">
#   <div style="max-width:600px; margin:auto; background:white; border-radius:10px;
#               box-shadow:0 2px 8px rgba(0,0,0,0.1); overflow:hidden;">

#     <div style="background:linear-gradient(135deg,#2563EB,#1D4ED8); padding:28px 32px;">
#       <h1 style="color:white; margin:0; font-size:22px;">🖥️ Technical Interview Invitation</h1>
#       <p style="color:#BFDBFE; margin:8px 0 0; font-size:14px;">{role} at {company}</p>
#     </div>

#     <div style="padding:28px 32px; color:#1F2937;">
#       <p style="font-size:15px;">Dear {candidate_name},</p>
#       <p style="font-size:15px; line-height:1.7;">
#         We are pleased to inform you that you have been selected to proceed to the
#         <strong style="color:#2563EB;">Technical Interview Round</strong> for the position of
#         <strong>{role}</strong> at <strong>{company}</strong>.
#       </p>

#       <div style="background:#EFF6FF; border-left:4px solid #2563EB; padding:14px 18px;
#                   border-radius:6px; margin:20px 0;">
#         <p style="margin:0; font-size:14px; color:#1E40AF;">
#           <strong>Round:</strong> Technical Interview<br>
#           <strong>Position:</strong> {role}<br>
#           <strong>Company:</strong> {company}
#         </p>
#       </div>

#       <p style="font-size:15px; line-height:1.7;">
#         Our team will reach out to you shortly with the schedule, format, and any preparation
#         materials for the technical round. Please ensure your availability and be prepared to
#         discuss your technical skills and past project experience.
#       </p>
#       <p style="font-size:15px; line-height:1.7;">
#         We look forward to speaking with you. Best of luck!
#       </p>

#       <hr style="border:none; border-top:1px solid #E5E7EB; margin:24px 0;">
#       <p style="font-size:14px; color:#6B7280; margin:0;">
#         Best Regards,<br>
#         <strong style="color:#1F2937;">{recruiter_name}</strong><br>
#         {recruiter_role}<br>
#         {recruiter_org}<br>
#         <em>AI Recruiter Agent</em>
#       </p>
#     </div>

#     <div style="background:#F9FAFB; padding:12px 32px; text-align:center;">
#       <p style="color:#9CA3AF; font-size:11px; margin:0;">
#         This email was sent by AI Recruiter Agent on behalf of {company}.
#       </p>
#     </div>
#   </div>
# </body>
# </html>
# """
#     return subject, body


# def _template_hr_round(candidate_name: str, role: str, company: str,
#                         recruiter_name: str, recruiter_role: str,
#                         recruiter_org: str) -> tuple[str, str]:
#     subject = f"HR Interview Invitation – {role} at {company}"
#     body = f"""
# <!DOCTYPE html>
# <html>
# <body style="font-family: Arial, sans-serif; background:#f4f4f4; padding:20px;">
#   <div style="max-width:600px; margin:auto; background:white; border-radius:10px;
#               box-shadow:0 2px 8px rgba(0,0,0,0.1); overflow:hidden;">

#     <div style="background:linear-gradient(135deg,#7C3AED,#6D28D9); padding:28px 32px;">
#       <h1 style="color:white; margin:0; font-size:22px;">🤝 HR Interview Invitation</h1>
#       <p style="color:#DDD6FE; margin:8px 0 0; font-size:14px;">{role} at {company}</p>
#     </div>

#     <div style="padding:28px 32px; color:#1F2937;">
#       <p style="font-size:15px;">Dear {candidate_name},</p>
#       <p style="font-size:15px; line-height:1.7;">
#         Congratulations on successfully clearing the Technical Round! We are excited to invite you
#         to the <strong style="color:#7C3AED;">HR Interview Round</strong> for the position of
#         <strong>{role}</strong> at <strong>{company}</strong>.
#       </p>

#       <div style="background:#F5F3FF; border-left:4px solid #7C3AED; padding:14px 18px;
#                   border-radius:6px; margin:20px 0;">
#         <p style="margin:0; font-size:14px; color:#5B21B6;">
#           <strong>Round:</strong> HR Interview<br>
#           <strong>Position:</strong> {role}<br>
#           <strong>Company:</strong> {company}
#         </p>
#       </div>

#       <p style="font-size:15px; line-height:1.7;">
#         During this round, we will discuss your background, career aspirations, compensation
#         expectations, and cultural fit with our organization. Please be prepared to share your
#         experiences and ask any questions you may have about the role and company.
#       </p>
#       <p style="font-size:15px; line-height:1.7;">
#         We will share the interview schedule details with you very soon. We're excited to learn
#         more about you!
#       </p>

#       <hr style="border:none; border-top:1px solid #E5E7EB; margin:24px 0;">
#       <p style="font-size:14px; color:#6B7280; margin:0;">
#         Best Regards,<br>
#         <strong style="color:#1F2937;">{recruiter_name}</strong><br>
#         {recruiter_role}<br>
#         {recruiter_org}<br>
#         <em>AI Recruiter Agent</em>
#       </p>
#     </div>

#     <div style="background:#F9FAFB; padding:12px 32px; text-align:center;">
#       <p style="color:#9CA3AF; font-size:11px; margin:0;">
#         This email was sent by AI Recruiter Agent on behalf of {company}.
#       </p>
#     </div>
#   </div>
# </body>
# </html>
# """
#     return subject, body


# # ── Core Email Functions ───────────────────────────────────────────────────────

# def _is_valid_email(email: str) -> bool:
#     """Validate email format."""
#     pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
#     return bool(re.match(pattern, email.strip()))


# def _get_smtp_connection() -> smtplib.SMTP:
#     """Create and return authenticated SMTP connection."""
#     if not SMTP_EMAIL or not SMTP_PASSWORD:
#         raise ValueError("SMTP credentials not configured. Add SMTP_EMAIL and SMTP_PASSWORD to .env file.")
#     server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
#     server.ehlo()
#     server.starttls()
#     server.login(SMTP_EMAIL, SMTP_PASSWORD)
#     return server


# def send_single_email(to_email: str, subject: str, html_body: str) -> dict:
#     """
#     Send a single HTML email.
#     Returns: {"success": bool, "error": str or None}
#     """
#     if not _is_valid_email(to_email):
#         return {"success": False, "error": f"Invalid email address: {to_email}"}

#     try:
#         msg = MIMEMultipart("alternative")
#         msg["Subject"] = subject
#         msg["From"]    = SMTP_EMAIL
#         msg["To"]      = to_email
#         msg.attach(MIMEText(html_body, "html"))

#         server = _get_smtp_connection()
#         server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
#         server.quit()
#         return {"success": True, "error": None}

#     except smtplib.SMTPAuthenticationError:
#         return {"success": False, "error": "SMTP authentication failed. Check SMTP_EMAIL and SMTP_PASSWORD in .env"}
#     except smtplib.SMTPRecipientsRefused:
#         return {"success": False, "error": f"Recipient refused: {to_email}"}
#     except smtplib.SMTPException as e:
#         return {"success": False, "error": f"SMTP error: {str(e)}"}
#     except Exception as e:
#         return {"success": False, "error": f"Unexpected error: {str(e)}"}


# def get_email_template(status: str, candidate_name: str, role: str, company: str,
#                         recruiter_name: str, recruiter_role: str,
#                         recruiter_org: str) -> Optional[tuple[str, str]]:
#     """
#     Get subject and HTML body for a given status.
#     Returns None for Pending (no email should be sent).
#     """
#     kwargs = dict(
#         candidate_name=candidate_name, role=role, company=company,
#         recruiter_name=recruiter_name, recruiter_role=recruiter_role,
#         recruiter_org=recruiter_org,
#     )
#     if status == "Selected":
#         return _template_selected(**kwargs)
#     elif status == "Rejected":
#         return _template_rejected(**kwargs)
#     elif status == "Technical Round":
#         return _template_technical_round(**kwargs)
#     elif status == "HR Round":
#         return _template_hr_round(**kwargs)
#     return None  # Pending — do not send


# def send_status_email(candidate: dict, drive: dict, recruiter: dict) -> dict:
#     """
#     Send status-appropriate email to a single candidate.
#     Returns log dict with delivery info.
#     """
#     status         = candidate.get("status", "Pending")
#     candidate_name = candidate.get("name",  "Candidate")
#     to_email       = candidate.get("email", "")
#     role           = drive.get("role",    "the role")
#     company        = drive.get("company", "our company")
#     recruiter_name = recruiter.get("name",         "Recruitment Team")
#     recruiter_role = recruiter.get("role",         "HR Manager")
#     recruiter_org  = recruiter.get("organization", company)

#     template = get_email_template(
#         status, candidate_name, role, company,
#         recruiter_name, recruiter_role, recruiter_org,
#     )

#     if template is None:
#         return {
#             "candidate_id":      str(candidate.get("_id", "")),
#             "candidate_name":    candidate_name,
#             "candidate_email":   to_email,
#             "status":            status,
#             "email_subject":     None,
#             "sent_by":           recruiter_name,
#             "sent_at":           datetime.utcnow(),
#             "delivery_status":   "skipped",
#             "error":             "Pending status — no email sent",
#         }

#     subject, html_body = template
#     result = send_single_email(to_email, subject, html_body)

#     return {
#         "candidate_id":    str(candidate.get("_id", "")),
#         "candidate_name":  candidate_name,
#         "candidate_email": to_email,
#         "status":          status,
#         "email_subject":   subject,
#         "sent_by":         recruiter_name,
#         "sent_at":         datetime.utcnow(),
#         "delivery_status": "sent" if result["success"] else "failed",
#         "error":           result.get("error"),
#     }


# def send_bulk_emails(candidates: list, drive: dict, recruiter: dict,
#                      progress_callback=None) -> dict:
#     """
#     Send emails to all non-pending candidates in bulk.
#     progress_callback(current, total) called after each email.

#     Returns summary dict:
#     {
#         "total":   int,
#         "sent":    int,
#         "failed":  int,
#         "skipped": int,
#         "logs":    list[dict],
#     }
#     """
#     logs    = []
#     sent    = 0
#     failed  = 0
#     skipped = 0
#     total   = len(candidates)

#     for i, candidate in enumerate(candidates):
#         log = send_status_email(candidate, drive, recruiter)
#         logs.append(log)

#         if log["delivery_status"] == "sent":
#             sent += 1
#         elif log["delivery_status"] == "failed":
#             failed += 1
#         else:
#             skipped += 1

#         if progress_callback:
#             progress_callback(i + 1, total)

#     return {
#         "total":   total,
#         "sent":    sent,
#         "failed":  failed,
#         "skipped": skipped,
#         "logs":    logs,
#     }


# def check_smtp_config() -> dict:
#     """Check if SMTP credentials are configured and valid."""
#     if not SMTP_EMAIL:
#         return {"configured": False, "error": "SMTP_EMAIL not set in .env"}
#     if not SMTP_PASSWORD:
#         return {"configured": False, "error": "SMTP_PASSWORD not set in .env"}
#     if not _is_valid_email(SMTP_EMAIL):
#         return {"configured": False, "error": f"SMTP_EMAIL '{SMTP_EMAIL}' is not a valid email"}
#     return {"configured": True, "error": None}




# modules/email_service.py
"""
Bulk email notification system for AI Recruiter Agent.
Uses Gmail SMTP SSL (port 465) with App Password from .env
"""

import os
import re
import smtplib
import logging
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465  # SSL — more reliable than 587/STARTTLS for App Passwords


# ── Credential helpers ────────────────────────────────────────────────────────

def _smtp_email() -> str:
    """Read SMTP_EMAIL fresh from env each call (safe after load_dotenv)."""
    return os.getenv("SMTP_EMAIL", "").strip()


def _smtp_password() -> str:
    """Read SMTP_PASSWORD fresh from env each call."""
    return os.getenv("SMTP_PASSWORD", "").strip()


def check_smtp_config() -> dict:
    """Return {configured: bool, error: str|None}."""
    email    = _smtp_email()
    password = _smtp_password()
    if not email:
        return {"configured": False, "error": "SMTP_EMAIL not set in .env"}
    if not password:
        return {"configured": False, "error": "SMTP_PASSWORD not set in .env"}
    if not _is_valid_email(email):
        return {"configured": False, "error": f"SMTP_EMAIL '{email}' is not a valid address"}
    return {"configured": True, "error": None}


def credentials_configured() -> bool:
    return check_smtp_config()["configured"]


# ── Validation ────────────────────────────────────────────────────────────────

def _is_valid_email(email: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$',
                         email.strip()))


# ── SMTP connection — SSL port 465 ────────────────────────────────────────────

def _get_smtp_connection() -> smtplib.SMTP_SSL:
    """
    Open an authenticated Gmail SMTP_SSL connection on port 465.
    This is the most reliable method for Gmail App Passwords.
    """
    email    = _smtp_email()
    password = _smtp_password()

    if not email or not password:
        raise ValueError(
            "SMTP credentials missing. Set SMTP_EMAIL and SMTP_PASSWORD in .env"
        )

    # Remove spaces from App Password if user copy-pasted with spaces
    # e.g. "dizx kkyz ycem qkve" → "dizxkkyzycemqkve"
    password = password.replace(" ", "")

    try:
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20)
        server.login(email, password)
        return server
    except smtplib.SMTPAuthenticationError:
        raise smtplib.SMTPAuthenticationError(
            535,
            b"Authentication failed. Make sure you are using a Gmail App Password "
            b"(not your Gmail login password). "
            b"Go to: Google Account > Security > 2-Step Verification > App Passwords"
        )


# ── Email templates ───────────────────────────────────────────────────────────

def _signature(recruiter_name: str, recruiter_role: str, recruiter_org: str) -> str:
    return f"""
    <hr style="border:none;border-top:1px solid #E5E7EB;margin:24px 0"/>
    <p style="font-size:13px;color:#6B7280;margin:0;line-height:1.8">
        Best Regards,<br/>
        <strong style="color:#1C1917">{recruiter_name}</strong><br/>
        {recruiter_role}<br/>
        {recruiter_org}
    </p>"""


def _wrap(header_color: str, header_html: str, body_html: str,
          company: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
</head>
<body style="font-family:'Segoe UI',Arial,sans-serif;background:#F5F2EE;margin:0;padding:20px">
  <div style="max-width:580px;margin:auto;background:#fff;border-radius:10px;
               border:1px solid #E2DBD4;overflow:hidden">
    <div style="background:{header_color};padding:26px 32px">
      {header_html}
    </div>
    <div style="padding:28px 32px;color:#1C1917;font-size:14px;line-height:1.75">
      {body_html}
    </div>
    <div style="background:#F5F2EE;padding:12px 32px;text-align:center;
                border-top:1px solid #E2DBD4">
      <p style="color:#9CA3AF;font-size:11px;margin:0">
        Sent by AI Recruiter on behalf of {company}
      </p>
    </div>
  </div>
</body>
</html>"""


def _template_selected(candidate_name: str, role: str, company: str,
                        recruiter_name: str, recruiter_role: str,
                        recruiter_org: str) -> tuple[str, str]:
    subject = f"Congratulations! You've Been Shortlisted \u2013 {role} at {company}"
    header  = """<h1 style="color:#fff;margin:0;font-size:20px;font-weight:600">
                    Congratulations!</h1>
                 <p style="color:#D1FAE5;margin:6px 0 0;font-size:13px">
                    You've been shortlisted</p>"""
    body = f"""
    <p>Dear <strong>{candidate_name}</strong>,</p>
    <p>We are delighted to inform you that after a thorough review of your application,
       you have been <strong style="color:#2D7A4F">shortlisted</strong> for:</p>
    <div style="background:#F0FDF4;border-left:4px solid #2D7A4F;border-radius:0 6px 6px 0;
                padding:12px 16px;margin:16px 0">
        <strong>Role:</strong> {role}<br/>
        <strong>Company:</strong> {company}
    </div>
    <p>Your profile closely matches what we are looking for. Our team will reach out
       shortly with details on the next steps. Please keep an eye on your inbox.</p>
    <p>Once again, congratulations — this reflects your hard work and dedication!</p>
    {_signature(recruiter_name, recruiter_role, recruiter_org)}"""
    return subject, _wrap("#2A7A4F", header, body, company)


def _template_rejected(candidate_name: str, role: str, company: str,
                        recruiter_name: str, recruiter_role: str,
                        recruiter_org: str) -> tuple[str, str]:
    subject = f"Application Update \u2013 {role} at {company}"
    header  = f"""<h1 style="color:#fff;margin:0;font-size:20px;font-weight:600">
                    Application Update</h1>
                  <p style="color:#E5E7EB;margin:6px 0 0;font-size:13px">
                    {role} at {company}</p>"""
    body = f"""
    <p>Dear <strong>{candidate_name}</strong>,</p>
    <p>Thank you for your interest in the <strong>{role}</strong> position at
       <strong>{company}</strong> and for the time you invested in our process.</p>
    <p>After careful consideration, we regret to inform you that we will not be moving
       forward with your application at this time. This was a competitive process and
       the decision was not a reflection of your abilities.</p>
    <div style="background:#FDF2F0;border-left:4px solid #C0622A;border-radius:0 6px 6px 0;
                padding:12px 16px;margin:16px 0;color:#7C2D12">
        We encourage you to apply for future openings that match your profile.
        We will keep your details on file.
    </div>
    <p>We wish you the very best in your career journey ahead.</p>
    {_signature(recruiter_name, recruiter_role, recruiter_org)}"""
    return subject, _wrap("#2C2825", header, body, company)


def _template_technical_round(candidate_name: str, role: str, company: str,
                                recruiter_name: str, recruiter_role: str,
                                recruiter_org: str) -> tuple[str, str]:
    subject = f"Technical Interview Invitation \u2013 {role} at {company}"
    header  = f"""<h1 style="color:#fff;margin:0;font-size:20px;font-weight:600">
                    Technical Interview Invitation</h1>
                  <p style="color:#BFDBFE;margin:6px 0 0;font-size:13px">
                    {role} at {company}</p>"""
    body = f"""
    <p>Dear <strong>{candidate_name}</strong>,</p>
    <p>We are pleased to invite you to the
       <strong style="color:#2E6DA0">Technical Interview Round</strong>
       for the position of <strong>{role}</strong> at <strong>{company}</strong>.</p>
    <div style="background:#EBF3FB;border-left:4px solid #2E6DA0;border-radius:0 6px 6px 0;
                padding:12px 16px;margin:16px 0">
        <strong>Round:</strong> Technical Interview<br/>
        <strong>Position:</strong> {role}<br/>
        <strong>Company:</strong> {company}
    </div>
    <p>Our team will contact you within <strong>2 business days</strong> to confirm
       the schedule, mode (virtual / in-person), and any preparation materials.</p>
    <p>We look forward to speaking with you. Best of luck!</p>
    {_signature(recruiter_name, recruiter_role, recruiter_org)}"""
    return subject, _wrap("#1E4E8A", header, body, company)


def _template_hr_round(candidate_name: str, role: str, company: str,
                        recruiter_name: str, recruiter_role: str,
                        recruiter_org: str) -> tuple[str, str]:
    subject = f"HR Interview Invitation \u2013 {role} at {company}"
    header  = f"""<h1 style="color:#fff;margin:0;font-size:20px;font-weight:600">
                    HR Interview Invitation</h1>
                  <p style="color:#DDD6FE;margin:6px 0 0;font-size:13px">
                    {role} at {company}</p>"""
    body = f"""
    <p>Dear <strong>{candidate_name}</strong>,</p>
    <p>Congratulations on progressing through the earlier rounds! We are pleased to
       invite you to the <strong style="color:#6B4F9E">HR Interview Round</strong>
       for <strong>{role}</strong> at <strong>{company}</strong>.</p>
    <div style="background:#F3EEF9;border-left:4px solid #6B4F9E;border-radius:0 6px 6px 0;
                padding:12px 16px;margin:16px 0">
        <strong>Round:</strong> HR Interview<br/>
        <strong>Position:</strong> {role}<br/>
        <strong>Company:</strong> {company}
    </div>
    <p>This round will cover career aspirations, compensation expectations, and
       cultural fit. We'll share scheduling details within <strong>2 business days</strong>.</p>
    <p>We are excited about the possibility of having you on the team!</p>
    {_signature(recruiter_name, recruiter_role, recruiter_org)}"""
    return subject, _wrap("#4C1D95", header, body, company)


def get_email_template(status: str, candidate_name: str, role: str, company: str,
                        recruiter_name: str, recruiter_role: str,
                        recruiter_org: str) -> Optional[tuple[str, str]]:
    """Return (subject, html_body) or None for Pending."""
    kw = dict(candidate_name=candidate_name, role=role, company=company,
              recruiter_name=recruiter_name, recruiter_role=recruiter_role,
              recruiter_org=recruiter_org)
    if status == "Selected":        return _template_selected(**kw)
    if status == "Rejected":        return _template_rejected(**kw)
    if status == "Technical Round": return _template_technical_round(**kw)
    if status == "HR Round":        return _template_hr_round(**kw)
    return None


# ── Core send ─────────────────────────────────────────────────────────────────

def send_single_email(to_email: str, subject: str, html_body: str) -> dict:
    """
    Send one HTML email via Gmail SSL.
    Returns {"success": bool, "error": str|None}
    """
    if not _is_valid_email(to_email):
        return {"success": False, "error": f"Invalid email address: {to_email}"}

    sender = _smtp_email()
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"AI Recruiter <{sender}>"
    msg["To"]      = to_email
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        server = _get_smtp_connection()
        server.sendmail(sender, to_email, msg.as_string())
        server.quit()
        return {"success": True, "error": None}
    except smtplib.SMTPAuthenticationError as e:
        return {"success": False, "error": (
            "Authentication failed. Use a Gmail App Password, not your regular password. "
            "Generate one at: Google Account → Security → 2-Step Verification → App Passwords"
        )}
    except smtplib.SMTPRecipientsRefused:
        return {"success": False, "error": f"Recipient refused by server: {to_email}"}
    except smtplib.SMTPConnectError as e:
        return {"success": False, "error": f"Cannot connect to Gmail SMTP: {e}"}
    except smtplib.SMTPException as e:
        return {"success": False, "error": f"SMTP error: {e}"}
    except OSError as e:
        return {"success": False, "error": f"Network error: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e}"}


def send_status_email(candidate: dict, drive: dict, recruiter: dict) -> dict:
    """
    Build and send the correct status email for one candidate.
    Returns a log dict ready to insert into MongoDB email_logs.
    """
    status         = candidate.get("status", "Pending")
    candidate_name = candidate.get("name",  "Candidate")
    to_email       = (candidate.get("email") or "").strip()
    role           = drive.get("role",    "the role")
    company        = drive.get("company", "our company")
    drive_id       = str(drive.get("_id", ""))
    recruiter_name = recruiter.get("name",         "Recruitment Team")
    recruiter_role = recruiter.get("role",         "HR Manager")
    recruiter_org  = recruiter.get("organization", company)
    sent_by        = str(recruiter.get("_id", recruiter_name))

    template = get_email_template(
        status, candidate_name, role, company,
        recruiter_name, recruiter_role, recruiter_org,
    )

    base_log = {
        "candidate_id":    str(candidate.get("_id", "")),
        "candidate_name":  candidate_name,
        "candidate_email": to_email,
        "drive_id":        drive_id,          # ← needed for history lookup
        "status":          status,
        "sent_by":         sent_by,
        "sent_at":         datetime.now(timezone.utc),
    }

    if template is None:
        return {**base_log, "email_subject": "", "delivery_status": "skipped",
                "error": "Pending — no email sent"}

    subject, html_body = template
    result = send_single_email(to_email, subject, html_body)

    return {
        **base_log,
        "email_subject":   subject,
        "delivery_status": "sent" if result["success"] else "failed",
        "error":           result.get("error"),
    }


# ── Bulk send ─────────────────────────────────────────────────────────────────

def send_bulk_emails(candidates: list, drive: dict, recruiter: dict,
                     progress_callback=None) -> dict:
    """
    Send status emails to all non-Pending candidates.
    Opens one SMTP connection and reuses it across all sends.

    progress_callback(current: int, total: int, name: str) — optional UI hook.

    Returns:
        {"total": int, "sent": int, "failed": int, "skipped": int, "logs": list}
    """
    EMAILABLE = {"Selected", "Rejected", "Technical Round", "HR Round"}
    logs    = []
    sent = failed = skipped = 0
    total   = len(candidates)

    # Open one shared connection for all emailable candidates
    shared_server: Optional[smtplib.SMTP_SSL] = None
    smtp_error: Optional[str] = None

    emailable_candidates = [c for c in candidates if c.get("status") in EMAILABLE]
    if emailable_candidates:
        try:
            shared_server = _get_smtp_connection()
        except Exception as e:
            smtp_error = str(e)

    sender = _smtp_email()

    for i, candidate in enumerate(candidates):
        status         = candidate.get("status", "Pending")
        candidate_name = candidate.get("name",  "Candidate")
        to_email       = (candidate.get("email") or "").strip()
        role           = drive.get("role",    "the role")
        company        = drive.get("company", "our company")
        drive_id       = str(drive.get("_id", ""))
        recruiter_name = recruiter.get("name",         "Recruitment Team")
        recruiter_role = recruiter.get("role",         "HR Manager")
        recruiter_org  = recruiter.get("organization", company)
        sent_by        = str(recruiter.get("_id", recruiter_name))

        if progress_callback:
            progress_callback(i + 1, total, candidate_name)

        base_log = {
            "candidate_id":    str(candidate.get("_id", "")),
            "candidate_name":  candidate_name,
            "candidate_email": to_email,
            "drive_id":        drive_id,
            "status":          status,
            "sent_by":         sent_by,
            "sent_at":         datetime.now(timezone.utc),
        }

        # Skip Pending
        if status not in EMAILABLE:
            skipped += 1
            logs.append({**base_log, "email_subject": "", "delivery_status": "skipped",
                         "error": "Pending — skipped"})
            continue

        # SMTP connection failed
        if shared_server is None:
            failed += 1
            logs.append({**base_log, "email_subject": "", "delivery_status": "failed",
                         "error": smtp_error or "Could not open SMTP connection"})
            continue

        template = get_email_template(
            status, candidate_name, role, company,
            recruiter_name, recruiter_role, recruiter_org,
        )
        if template is None:
            skipped += 1
            logs.append({**base_log, "email_subject": "", "delivery_status": "skipped",
                         "error": "No template for status"})
            continue

        subject, html_body = template

        if not _is_valid_email(to_email):
            failed += 1
            logs.append({**base_log, "email_subject": subject, "delivery_status": "failed",
                         "error": f"Invalid email: {to_email}"})
            continue

        # Send using shared connection
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"AI Recruiter <{sender}>"
        msg["To"]      = to_email
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        try:
            shared_server.sendmail(sender, to_email, msg.as_string())
            sent += 1
            logs.append({**base_log, "email_subject": subject,
                         "delivery_status": "sent", "error": None})
        except smtplib.SMTPRecipientsRefused:
            failed += 1
            logs.append({**base_log, "email_subject": subject, "delivery_status": "failed",
                         "error": f"Recipient refused: {to_email}"})
        except smtplib.SMTPServerDisconnected:
            # Try to reconnect once
            try:
                shared_server = _get_smtp_connection()
                shared_server.sendmail(sender, to_email, msg.as_string())
                sent += 1
                logs.append({**base_log, "email_subject": subject,
                             "delivery_status": "sent", "error": None})
            except Exception as e:
                failed += 1
                logs.append({**base_log, "email_subject": subject, "delivery_status": "failed",
                             "error": f"Reconnect failed: {e}"})
        except Exception as e:
            failed += 1
            logs.append({**base_log, "email_subject": subject, "delivery_status": "failed",
                         "error": str(e)})

    if shared_server:
        try:
            shared_server.quit()
        except Exception:
            pass

    return {"total": total, "sent": sent, "failed": failed,
            "skipped": skipped, "logs": logs}


# ── Log helpers ───────────────────────────────────────────────────────────────

def save_email_logs(db, logs: list[dict]) -> None:
    """Bulk-insert email log dicts into the email_logs collection."""
    if logs:
        try:
            db.email_logs.insert_many(logs, ordered=False)
        except Exception as e:
            logger.warning("Failed to save email logs: %s", e)


def get_email_logs(db, drive_id: str) -> list[dict]:
    """Return all email logs for a drive, newest first."""
    return list(db.email_logs.find({"drive_id": drive_id}).sort("sent_at", -1))