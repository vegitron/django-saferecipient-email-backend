"""SMTP email backend class that only sends email to a safe email address"""
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend
from email.mime.text import MIMEText
from django.conf import settings

class EmailBackend(SMTPEmailBackend):
    """
    Re-routes email, so it goes to, and comes from
    settings.SAFE_EMAIL_RECIPIENT.

    The original to and from are added to a text file
    that is attached to the message.
    """
    def send_messages(self, email_messages):
        for message in email_messages:
            originals = "Originally sent from: %s\nOriginally sent to: %s\n" % (
                message.from_email, tuple(message.recipients()))

            message.from_email = settings.SAFE_EMAIL_RECIPIENT
            message.to = [settings.SAFE_EMAIL_RECIPIENT]
            text_attachment = MIMEText(originals)
            text_attachment.add_header("Content-disposition",
                'attachment; filename="original_emails.txt"')
            message.attach(text_attachment)
        return super(EmailBackend, self).send_messages(email_messages)
