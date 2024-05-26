import base64
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition,Bcc
from django.core.files.base import ContentFile
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, MimeType
from django.template.loader import render_to_string
from django.conf import settings

# Replace the following variables with your own values
api_key = settings.SENDGRID_API_KEY
from_email = 'activitypointsengg@gmail.com'
from_communications_email = 'communications@activitypointsengg.com'
from_promotions1_email = 'promotions1@lgstrust.com'
subject = 'Test Email'
plain_text_content = 'This is a test email sent using SendGrid.'
html_content = '<p>This is a test email sent using <strong>SendGrid</strong>.</p>'
static_to_email = 'lgstrustindia@gmail.com'


def send_activity_report_email(to_email_user, order_detail, ):
    context = {
        "email": to_email_user,
        "order_detail": order_detail,
        "first_name": order_detail.order.user.first_name if order_detail.order.user.first_name else "Student",
        "base_url": settings.PROJECT_BASE_URL,
        "title_subject": "REPORT and CERTIFICATE – ACTIVITY POINTS ENGG APP",
        "protocol": "https"
        if getattr(settings, "FRONTEND_USE_HTTPS", False)
        else "http",
    }
    email_html_content = render_to_string("email/generation_of_report.html", context)
    email_subject = "REPORT and CERTIFICATE – ACTIVITY POINTS ENGG APP"
    # Create a Mail object
    mail = Mail(
        from_email=from_communications_email,
        to_emails=to_email_user,
        subject=email_subject,
    )

    # Add HTML content
    html = Content(MimeType.html, email_html_content)
    mail.add_content(html)

    # Read file content
    attachment_content = ContentFile(order_detail.report_file.read())
    attachment_filename = order_detail.report_file.name

    # Convert binary data to base64-encoded string
    attachment_content_base64 = base64.b64encode(attachment_content.read()).decode("utf-8")

    # Create an Attachment object
    attachment = Attachment()
    attachment.file_content = FileContent(attachment_content_base64)
    attachment.file_name = FileName(attachment_filename)
    attachment.file_type = FileType("application/pdf")
    attachment.disposition = Disposition("attachment")

    # Attach the file to the email
    mail.attachment = attachment

    # Initialize the SendGrid API client with your SendGrid API key
    sg = SendGridAPIClient(api_key)

    # Send the email
    try:
        response = sg.send(mail)
    except Exception as e:
        print(f"Error sending email: {e}")


def send_order_invoice_email(order):
    context = {
        "email": order.user.email,
        "first_name": order.user.first_name if order.user.first_name else "Student",
        "base_url": settings.PROJECT_BASE_URL,
        "title_subject": "Activity Subscription Successful – ACTIVITY POINTS ENGG APP",
        "protocol": "https"
        if getattr(settings, "FRONTEND_USE_HTTPS", False)
        else "http",
    }
    email_html_content = render_to_string("email/generation_of_invoice.html", context)
    email_subject = "Activity Subscription Successful – ACTIVITY POINTS ENGG APP"

    # Create a Mail object
    mail = Mail(
        from_email=from_communications_email,
        to_emails=[order.user.email,],
        subject=email_subject,
    )

    # Add HTML content
    html = Content(MimeType.html, email_html_content)
    mail.add_content(html)

    # Read file content
    attachment_content = ContentFile(order.invoice_file.read())
    attachment_filename = order.invoice_file.name

    # Convert binary data to base64-encoded string
    attachment_content_base64 = base64.b64encode(attachment_content.read()).decode("utf-8")

    # Create an Attachment object
    attachment = Attachment()
    attachment.file_content = FileContent(attachment_content_base64)
    attachment.file_name = FileName(attachment_filename)
    attachment.file_type = FileType("application/pdf")
    attachment.disposition = Disposition("attachment")

    # Attach the file to the email
    mail.attachment = attachment

    # Initialize the SendGrid API client with your SendGrid API key
    sg = SendGridAPIClient(api_key)

    try:
        # Send the email
        response = sg.send(mail)

        # Log the success or additional details
        print(f"Email sent. Status code: {response.status_code}")

    except Exception as e:
        # Log the error or take appropriate action
        print(f"Error sending email: {e}")


def sub_admin_reset_password_mail(user, reset_link):
    # Replace 'YOUR_FROM_EMAIL' and 'YOUR_SENDGRID_API_KEY' with your actual values

    context = {
        "user": user,
        "reset_link": reset_link,
        "protocol": "https" if getattr(settings, "FRONTEND_USE_HTTPS", False) else "http",
    }
    email_html_content = render_to_string("email/sub_admin_reset_password.html", context)
    email_subject = "“Activity Points Portal: Password Reset”"

    # Create a Mail object
    mail = Mail(
        from_email=from_email,
        to_emails=user.email,
        subject=email_subject,
    )

    # Add HTML content
    html = Content(MimeType.html, email_html_content)
    mail.add_content(html)

    # Initialize the SendGrid API client with your SendGrid API key
    sg = SendGridAPIClient(api_key)

    # Send the email
    try:
        response = sg.send(mail)
        print(response.__dict__)
    except Exception as e:
        print(f"Error sending email: {e}")


def send_email_download_student(email, first_name):
    context = {
        "email": email,
        "first_name": first_name,
        "base_url": settings.PROJECT_BASE_URL,
        "protocol": "https" if getattr(settings, "FRONTEND_USE_HTTPS", False) else "http",
    }
    email_html_content = render_to_string("email/download_mail.html", context)
    email_subject = "Download Notification - Your Company Name"

    # Create a Mail object
    mail = Mail(
        from_email=from_email,
        to_emails=email,
        subject=email_subject,
    )

    # Add HTML content
    html = Content(MimeType.html, email_html_content)
    mail.add_content(html)

    # Initialize the SendGrid API client with your SendGrid API key
    sg = SendGridAPIClient(api_key)

    # Send the email
    try:
        response = sg.send(mail)
    except Exception as e:
        print(f"Error sending email: {e}")


def verify_otp_sing_up(email, otp):
    context = {
        "email": email,
        "first_name": "Student",
        "otp": otp,
        "base_url": settings.PROJECT_BASE_URL,
        "protocol": "https" if getattr(settings, "FRONTEND_USE_HTTPS", False) else "http",
    }
    email_html_content = render_to_string("email/verify_otp_sing_up.html", context)
    email_subject = "OTP Verification - ACTIVITY POINTS ENGG APP"

    # Create a Mail object
    mail = Mail(
        from_email=from_communications_email,
        to_emails=email,
        subject=email_subject,
    )

    # Add HTML content
    html = Content(MimeType.html, email_html_content)
    mail.add_content(html)

    # Initialize the SendGrid API client with your SendGrid API key
    sg = SendGridAPIClient(api_key)

    # Send the email
    try:
        response = sg.send(mail)
    except Exception as e:
        print(f"Error sending email: {e}")


def sing_up_successful(user, password):
    context = {
        "user": user,
        "first_name": user.first_name,
        "password": password,
        "title_subject": "Successful SIGNUP – ACTIVITY POINTS ENGG APP",
        "base_url": settings.PROJECT_BASE_URL,
        "protocol": "https" if getattr(settings, "FRONTEND_USE_HTTPS", False) else "http",
    }
    email_html_content = render_to_string("email/singup_successful.html", context)
    email_subject = "Successful Signup - ACTIVITY POINTS ENGG APP"

    # Create a Mail object
    mail = Mail(
        from_email=from_communications_email,
        to_emails=user.email,
        subject=email_subject,
    )

    # Add HTML content
    html = Content(MimeType.html, email_html_content)
    mail.add_content(html)

    # Initialize the SendGrid API client with your SendGrid API key
    sg = SendGridAPIClient(api_key)

    # Send the email
    try:
        response = sg.send(mail)
    except Exception as e:
        print(f"Error sending email: {e}")


def forget_password_otp(user, otp):
    context = {
        "user": user,
        "otp": otp,
        "first_name": user.first_name if user.first_name else "Student",
        "title_subject": "PASSWORD Reset OTP – ACTIVITY POINTS ENGG APP",
        "base_url": settings.PROJECT_BASE_URL,
        "protocol": "https" if getattr(settings, "FRONTEND_USE_HTTPS", False) else "http",
    }
    email_html_content = render_to_string("email/forget_password_otp.html", context)
    email_subject = "Password Reset OTP - ACTIVITY POINTS ENGG APP"

    # Create a Mail object
    mail = Mail(
        from_email=from_communications_email,
        to_emails=user.email,
        subject=email_subject,
    )

    # Add HTML content
    html = Content(MimeType.html, email_html_content)
    mail.add_content(html)

    # Initialize the SendGrid API client with your SendGrid API key
    sg = SendGridAPIClient(api_key)

    # Send the email
    try:
        response = sg.send(mail)
    except Exception as e:
        print(f"Error sending email: {e}")


def send_notification_email(user, title, message):
    # Replace 'YOUR_FROM_EMAIL' and 'YOUR_SENDGRID_API_KEY' with your actual values

    context = {
        "user": user,
        "first_name": user.first_name if user.first_name else "Student",
        "title_subject": title,
        "message": message,
        "base_url": settings.PROJECT_BASE_URL,
        "protocol": "https" if getattr(settings, "FRONTEND_USE_HTTPS", False) else "http",
    }
    email_html_content = render_to_string("email/notification_email.html", context)
    email_subject = f"{title} - ADMIN NOTIFICATION – ACTIVITY POINTS ENGG APPLICATION"  # Modify as needed

    # Create a Mail object
    mail = Mail(
        from_email=from_communications_email,
        to_emails=user.email,
        subject=email_subject,
    )

    # Add HTML content
    html = Content(MimeType.html, email_html_content)
    mail.add_content(html)

    # Initialize the SendGrid API client with your SendGrid API key
    sg = SendGridAPIClient(api_key)

    # Send the email
    try:
        response = sg.send(mail)
    except Exception as e:
        print(f"Error sending email: {e}")


def send_promotional_email(user, subject, body):
    context = {
        "user": user,
        "title_subject": "Promotional Email",
        "subject": subject,
        "body": body,
        "base_url": settings.PROJECT_BASE_URL,
        "protocol": "https" if getattr(settings, "FRONTEND_USE_HTTPS", False) else "http",
    }
    email_html_content = render_to_string("email/promotional_email.html", context)

    # Create a Mail object
    mail = Mail(
        from_email=from_promotions1_email,
        to_emails=static_to_email,  # Adjust as needed based on your requirements
        subject=subject,
    )
    for user_email in user:
        mail.add_bcc(user_email)

    # Add HTML content
    html = Content(MimeType.html, email_html_content)
    mail.add_content(html)

    # Initialize the SendGrid API client with your SendGrid API key
    sg = SendGridAPIClient(api_key)

    # Send the email
    try:
        response = sg.send(mail)
    except Exception as e:
        print(f"Error sending email: {e}")
