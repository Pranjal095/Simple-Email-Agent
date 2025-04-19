import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import email_config

class EmailSender:
    def __init__(self, smtp_server=None, smtp_port=None, email_address=None, email_password=None):
        self.smtp_server = smtp_server or email_config.smtp_server
        self.smtp_port = smtp_port or email_config.smtp_port
        self.email_address = email_address or email_config.email_address
        self.email_password = email_password or email_config.email_password
    
    def send_email(self, to_email, subject, content):
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(content, 'plain'))
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)
            
            text = msg.as_string()
            server.sendmail(self.email_address, to_email, text)
            
            server.quit()
            return True, "Email sent successfully!"
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"