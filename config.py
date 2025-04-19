import os
import dotenv
from pydantic import BaseModel

dotenv.load_dotenv()

class EmailConfig(BaseModel):
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", 587))
    email_address: str = os.getenv("EMAIL_ADDRESS", "")
    email_password: str = os.getenv("EMAIL_PASSWORD", "")
    model_path: str = os.getenv("MODEL_PATH", "")

email_config = EmailConfig()