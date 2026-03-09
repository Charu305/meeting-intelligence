import smtplib
from email.message import EmailMessage

def send_email(to, subject, body):

    sender = "charunyavenkatesan@gmail.com"
    password = "qohenwhztqhvtfmm"   # Gmail app password

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

    return "Email sent successfully"
