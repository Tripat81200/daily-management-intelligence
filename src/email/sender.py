import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)


class EmailSender:
    """Delivers newsletters via Resend API or SMTP (Gmail/Custom)."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.email_cfg = config.get("email", {})
        self.service = self.email_cfg.get("service", "resend").lower()
        self.to_address = self.email_cfg.get("to") or os.getenv("EMAIL_TO")
        self.from_address = self.email_cfg.get("from_address", "Management Intelligence <onboarding@resend.dev>")
        self.resend_api_key = self.email_cfg.get("resend_api_key") or os.getenv("RESEND_API_KEY")
        self.smtp_host = self.email_cfg.get("smtp_host") or os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(self.email_cfg.get("smtp_port") or os.getenv("SMTP_PORT", 587))
        self.smtp_user = self.email_cfg.get("smtp_user") or os.getenv("SMTP_USER")
        self.smtp_pass = self.email_cfg.get("smtp_pass") or os.getenv("SMTP_PASS")

    def send(self, subject: str, html_body: str, plain_text_body: str, dry_run: bool = False) -> bool:
        """Send the briefing via configured provider or save dry run output."""
        output_file = Path(__file__).resolve().parent.parent.parent / "data" / "sample_briefing.html"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_body)

        if dry_run:
            logger.info(f"DRY RUN enabled. Email not sent across network. Saved preview to {output_file}")
            print(f"\n[DRY RUN SUCCESS] Rendered newsletter saved to: {output_file}")
            print(f"Subject: {subject}")
            print(f"Recipient: {self.to_address or 'None specified'}\n")
            return True

        if not self.to_address:
            raise ValueError(
                "Recipient email is missing! Please set EMAIL_TO in your environment or GitHub Secrets."
            )

        if self.service == "resend" or (self.resend_api_key and not self.smtp_user):
            return self._send_via_resend(subject, html_body, plain_text_body)
        elif self.smtp_user and self.smtp_pass:
            return self._send_via_smtp(subject, html_body, plain_text_body)
        else:
            logger.warning(
                "No valid email credentials found (neither RESEND_API_KEY nor SMTP_USER/SMTP_PASS). "
                f"Saving briefing locally to {output_file}"
            )
            return False

    def _send_via_resend(self, subject: str, html_body: str, plain_text_body: str) -> bool:
        if not self.resend_api_key:
            raise ValueError("RESEND_API_KEY is missing for Resend email delivery.")

        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {self.resend_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "from": self.from_address,
            "to": [self.to_address],
            "subject": subject,
            "html": html_body,
            "text": plain_text_body
        }

        logger.info(f"Sending email via Resend to {self.to_address}...")
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        if resp.status_code in (200, 201):
            data = resp.json()
            logger.info(f"Email delivered successfully via Resend. ID: {data.get('id')}")
            return True
        else:
            logger.error(f"Failed to send email via Resend: HTTP {resp.status_code} - {resp.text}")
            raise RuntimeError(f"Resend delivery failed: {resp.text}")

    def _send_via_smtp(self, subject: str, html_body: str, plain_text_body: str) -> bool:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.from_address or self.smtp_user
        msg["To"] = self.to_address

        part1 = MIMEText(plain_text_body, "plain", "utf-8")
        part2 = MIMEText(html_body, "html", "utf-8")
        msg.attach(part1)
        msg.attach(part2)

        logger.info(f"Connecting to SMTP server {self.smtp_host}:{self.smtp_port}...")
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=25) as server:
                server.ehlo()
                if self.smtp_port in (587, 25):
                    server.starttls()
                    server.ehlo()
                server.login(self.smtp_user, self.smtp_pass)
                server.sendmail(msg["From"], [self.to_address], msg.as_string())
            logger.info(f"Email sent successfully via SMTP to {self.to_address}")
            return True
        except Exception as e:
            logger.error(f"Failed to deliver email via SMTP: {e}")
            raise
