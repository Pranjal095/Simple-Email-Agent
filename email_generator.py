from llama_cpp import Llama
from config import email_config

class EmailGenerator:
    def __init__(self, model_path=None):
        self.model_path = model_path or email_config.model_path
        print(f"Loading Llama model from: {self.model_path}")
        self.model = Llama(model_path=self.model_path)
    
    def generate_email(self, prompt):
        system_prompt = """
        You are an AI email assistant acting on behalf of Pranjal Prajapati for sending email to a given recipient. Generate a fully cohesive playfully formal email with a single subject line and content as per the user given description. 
        
        The response should be in the format:
        Subject: [Email Subject]
        
        [Email Body Content]
        
        [Always end with a closing like "Regards," or "Best regards," followed by "Pranjal Prajapati" alone and nothing else from next line onwards]

        Only generate a single email. End your response after the email signature.
        """
        
        full_prompt = f"{system_prompt}\n\nUser request: {prompt}"
        
        output = self.model.create_completion(
            prompt=full_prompt,
            temperature=0.6,
            max_tokens=7000,
            top_p=0.9,
            stop=["---", "###", "Subject:"]
        )
        
        generated_text = output['choices'][0]['text']
        
        try:
            parts = generated_text.split("Subject:", 1)
            if len(parts) > 1:
                subject_and_content = parts[1].strip()
                if "\n\n" in subject_and_content:
                    subject, content = subject_and_content.split("\n\n", 1)
                    content = content.split("\n\nSubject:", 1)[0].split("\n\n---", 1)[0].strip()
                    return self.refine_email(subject.strip(), content.strip(), prompt)
                else:
                    return subject_and_content.strip(), ""
            else:
                text = generated_text.strip()
                lines = text.split("\n")
                subject = lines[0]
                content = "\n".join(lines[1:])
                return self.refine_email(subject, content, prompt)
        except Exception as e:
            print(f"Error parsing email: {e}")
            return "Generated Email", generated_text
    
    def refine_email(self, subject, content, original_prompt):
        reflection_prompt = f"""
        You are an expert email editor. Review and improve the following email while maintaining its core message and intent.
        
        Original request: {original_prompt}
        
        Current email:
        Subject: {subject}
        
        {content}
        
        Provide an improved version with these guidelines:
        - Ensure the subject is concise and engaging
        - Check for appropriate tone, formality, and clarity
        - Improve structure and flow
        - Fix any grammatical or spelling errors
        - Make sure it sounds natural (playful) and professional
        - ALWAYS end with a closing like "Regards," or "Best regards," followed by "Pranjal Prajapati"
        
        Respond ONLY with the refined email in this format:
        Subject: [Improved Subject]
        
        [Improved Email Content ending with a closing signature]
        """
        
        output = self.model.create_completion(
            prompt=reflection_prompt,
            temperature=0.5,
            max_tokens=7000,
            top_p=0.9,
            stop=["---", "###"]
        )
        
        refined_text = output['choices'][0]['text']
        
        try:
            parts = refined_text.split("Subject:", 1)
            if len(parts) > 1:
                subject_and_content = parts[1].strip()
                if "\n\n" in subject_and_content:
                    refined_subject, refined_content = subject_and_content.split("\n\n", 1)
                    refined_content = refined_content.split("\n\nSubject:", 1)[0].split("\n\n---", 1)[0].strip()
                    return refined_subject.strip(), refined_content.strip()
                else:
                    return subject_and_content.strip(), ""
            else:
                print("Reflection failed to parse properly. Returning original.")
                return subject, content
        except Exception as e:
            print(f"Error in reflection: {e}")
            return subject, content