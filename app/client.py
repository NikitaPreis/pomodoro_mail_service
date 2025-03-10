from dataclasses import dataclass
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart

from app.settings import Settings


@dataclass
class MailClient:
    settings: Settings

    def send_email_task(
        self, subject: str, text: str, to: str
    ) -> None:
        msg = self._build_message(subject=subject, text=text, to=to)
        self._send_email(msg=msg)


    def _build_message(
        self, subject: str, text: str, to: str
    ) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg['From'] = self.settings.FROM_EMAIL
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEMultipart(text, 'plain'))
        return msg


    def _send_email(self, msg: MIMEMultipart):
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(
            self.settings.SMTP_HOST, self.settings.SMTP_PORT, context=context
        )
        server.login(self.settings.FROM_EMAIL, self.settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
