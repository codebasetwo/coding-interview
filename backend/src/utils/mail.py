from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from backend.src.config import Config

EMAIL_CONF = ConnectionConfig(
    MAIL_DEBUG=True,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_PORT=Config.MAIL_PORT,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

FM = FastMail(EMAIL_CONF)

def create_message(subject: str, recipients: list[str], body: str) -> MessageSchema:
    """Create an email message to send.

    Args:
        subject (str): The subject of the email.
        email (list[str]): The recipient email addresses.
        body (str): The body of the email.

    Returns:
        MessageSchema: The email message to send.
    """
    return MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html
    )


email_verification_message = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verify Your Email</title>
  <style>
    body {{
      font-family: 'Segoe UI', sans-serif;
      background-color: #f4f4f4;
      margin: 0;
      padding: 0;
    }}
    .container {{
      max-width: 600px;
      margin: auto;
      background-color: #ffffff;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .header {{
      text-align: center;
      padding-bottom: 20px;
    }}
    .header h1 {{
      color: #333333;
    }}
    .content {{
      font-size: 16px;
      color: #555555;
      line-height: 1.6;
    }}
    .button {{
      display: block;
      width: fit-content;
      margin: 30px auto;
      padding: 12px 24px;
      background-color: #0078D4;
      color: #ffffff;
      text-decoration: none;
      border-radius: 5px;
      font-weight: bold;
    }}
    .footer {{
      text-align: center;
      font-size: 12px;
      color: #999999;
      margin-top: 20px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Welcome to the Interview 🎉</h1>
    </div>
    <div class="content">
      <p>Hi {full_name},</p>
      <p>Thanks for signing up! To get started, please verify your email address by clicking the button below:</p>
      <a href="{verification_link}" class="button">Verify Email</a>
      <p>If you didn’t sign up for Interview, you can safely ignore this email.</p>
    </div>
    <div class="footer">
      &copy; 2025 Codebasetwo. All rights reserved.
    </div>
  </div>
</body>
</html>
"""

password_message_template = """
    <h1>Reset Your Password</h1>
    <p>Please click this <a href="{url}">link</a> to Reset Your Password</p>
    <p>If you didn’t make this request. please let us know.</p>
    """