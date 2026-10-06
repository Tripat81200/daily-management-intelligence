from pathlib import Path
from src.email.sender import EmailSender


def test_email_sender_dry_run():
    cfg = {
        "email": {
            "to": "test@example.com",
            "service": "resend",
            "from_address": "Test <test@resend.dev>"
        }
    }
    sender = EmailSender(cfg)
    html_sample = "<html><body><h1>Test Newsletter</h1></body></html>"
    text_sample = "Test Newsletter"

    success = sender.send(
        subject="Test Subject",
        html_body=html_sample,
        plain_text_body=text_sample,
        dry_run=True
    )
    assert success is True

    preview_file = Path(__file__).resolve().parent.parent / "data" / "sample_briefing.html"
    assert preview_file.exists()
    with open(preview_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Test Newsletter" in content
