import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import render_template, current_app
from datetime import datetime

# Edit these
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "24034211086@gnu.ac.in"  # Set to your Gmail (App Password required)
SENDER_PASSWORD = "wntn picx fqwx brzm"  # App Password, never your regular Gmail password

def send_email(
    subject,
    recipient,
    body,
    html_body=None,
    attachment_data=None,
    attachment_name=None
):
    """
    Send email with optional HTML and attachment.

    Args:
        subject (str): Email subject
        recipient (str): Recipient email address
        body (str): Plain text body
        html_body (str, optional): HTML body
        attachment_data (bytes, optional): Attachment file bytes
        attachment_name (str, optional): Name for the attachment

    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        msg = MIMEMultipart('mixed')
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject

        # Alternative part: plain text and HTML
        text_part = MIMEText(body, 'plain')
        alt_part = MIMEMultipart('alternative')
        alt_part.attach(text_part)

        if html_body:
            html_part = MIMEText(html_body, 'html')
            alt_part.attach(html_part)

        msg.attach(alt_part)

        # Attachment part
        if attachment_data and attachment_name:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_data)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{attachment_name}"')
            msg.attach(part)

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
        server.quit()

        print(f"✅ Email sent successfully to {recipient}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email to {recipient}: {e}")
        return False

def send_certificate_email_flask(
    student, event, pdf_data, download_url
):
    """
    Compose and send a creative certificate email (to use in your Flask routes).

    Args:
        student: Student model (must have .name and .email)
        event: Event model (must have .title, .organizer, .event_type, .date, .location)
        pdf_data (bytes): Certificate PDF bytes
        download_url (str): External download link for certificate (from url_for(..., _external=True))
    """
    subject = f"🏆 Your Certificate - {event.title}"
    plain_body = f"""Dear {student.name},

Congratulations! Your certificate for the event "{event.title}" is ready.

You can download your certificate here: {download_url}

Best regards,
{event.organizer}
"""

    html_body = render_template(
        "email_certificate.html",
        subject=subject,
        recipient_name=student.name,
        event=event,
        certificate_download_url=download_url,
        current_year=datetime.now().year
    )

    return send_email(
        subject=subject,
        recipient=student.email,
        body=plain_body,
        html_body=html_body,
        attachment_data=pdf_data,
        attachment_name=f"{student.name}_certificate.pdf"
    )

# Optional: test function to verify config
def test_email_config():
    result = send_email(
        subject="Test Email from CertManager",
        recipient="test@example.com",
        body="This is a test email to verify configuration."
    )
    return result

# Run a config test if executed directly
if __name__ == "__main__":
    print("Testing email configuration...")
    test_result = test_email_config()
    print(f"Test result: {'✅ Success' if test_result else '❌ Failed'}")
