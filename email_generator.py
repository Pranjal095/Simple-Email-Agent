from llama_cpp import Llama
from config import email_config

class EmailGenerator:
    def __init__(self, model_path=None):
        self.model_path = model_path or email_config.model_path
        print(f"Loading Llama model from: {self.model_path}")
        self.model = Llama(model_path=self.model_path)
    
    def generate_email(self, prompt, recipient=None):
        system_prompt = """
        You are an AI email assistant acting on behalf of Pranjal Prajapati for sending email to given recipient email. Generate a fully cohesive playfully formal email with a single subject line and content as per the user given description. Final response should only include subject and content to be sent directly.
        The response should be in the format:
        Subject: [Email Subject]
        
        [Email Body Content]

        Only generate a single email. End your response after the email body content.
        """
        
        if recipient:
            context = f"The email is being sent to {recipient}."
            full_prompt = f"{system_prompt}\n\nContext: {context}\n\nUser request: {prompt}"
        else:
            full_prompt = f"{system_prompt}\n\nUser request: {prompt}"
        
        output = self.model.create_completion(
            prompt=full_prompt,
            temperature=0.7,
            max_tokens=7000,
            top_p=0.9,
        )
        
        generated_text = output['choices'][0]['text']
        
        try:
            parts = generated_text.split("Subject:", 1)
            if len(parts) > 1:
                subject_and_content = parts[1].strip()
                if "\n\n" in subject_and_content:
                    subject, content = subject_and_content.split("\n\n", 1)
                    content = content.split("\n\nSubject:", 1)[0].split("\n\n---", 1)[0].strip()
                    return subject.strip(), content.strip()
                else:
                    return subject_and_content.strip(), ""
            else:
                text = generated_text.strip()
                lines = text.split("\n")
                subject = lines[0]
                content = "\n".join(lines[1:])
                return subject, content
        except Exception as e:
            print(f"Error parsing email: {e}")
            return "Generated Email", generated_text