import frappe
from frappe.email import sendmail_to_system_user

@frappe.whitelist()
def get_user_email_accounts():
    user_email_accounts = frappe.get_all(
        "User Email",
        filters={"user": frappe.session.user, "awaiting_password": 0},
        fields=["email_account", "email_id"],
    )
    if not user_email_accounts:
        return []
        
    return frappe.get_all(
        "Email Account",
        filters={"name": ["in", [d.email_account for d in user_email_accounts]]},
        fields=["email_id", "name"],
    )

@frappe.whitelist()
def send_mail(
    recipients,
    sender,
    subject,
    content,
    cc=None,
    bcc=None,
    attachments=None,
    communication=None,
    doctype=None,
    name=None,
):
    if not sender:
        frappe.throw(frappe._("Please select a sender"))

    if not recipients:
        frappe.throw(frappe._("Please select at least one recipient"))

    if isinstance(recipients, str):
        recipients = recipients.split(",")
    if isinstance(cc, str):
        cc = cc.split(",")
    if isinstance(bcc, str):
        bcc = bcc.split(",")

    sendmail_to_system_user(
        subject=subject,
        content=content,
        sender=sender,
        recipients=recipients,
        cc=cc,
        bcc=bcc,
        attachments=attachments,
        message_id=communication,
        reference_doctype=doctype,
        reference_name=name,
    )
