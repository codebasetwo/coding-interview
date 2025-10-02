from asgiref.sync import async_to_sync
from celery import Celery

from backend.src.utils.mail import create_message, FM


celery_app = Celery(__name__)
celery_app.config_from_object("src.config")

@celery_app.task()
def send_email_task(subject: str, recipients: list[str], body: str) -> dict[str, str]:
    """Send an email using the FastMail configuration."""
    message = create_message(subject, recipients, body)
    try:
        async_to_sync(FM.send_message)(message)
        return {"status": "success", "message": "Email sent successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}