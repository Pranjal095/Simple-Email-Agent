import os
import sys
import argparse
from email_generator import EmailGenerator
from email_sender import EmailSender

def print_banner():
    banner = """
    =======================================
    =      AI Email Assistant System      =
    =======================================
    """
    print(banner)

def get_multiline_input(prompt):
    print(prompt)
    print("(Type 'END' on a new line to finish)")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description='AI Email Assistant')
    parser.add_argument('--model', help='Path to Llama model file', default=None)
    args = parser.parse_args()
    
    clear_screen()
    print_banner()
    
    try:
        print("Initializing email generator...")
        email_generator = EmailGenerator(model_path=args.model)
        print("Initializing email sender...")
        email_sender = EmailSender()
    except Exception as e:
        print(f"Error initializing components: {str(e)}")
        sys.exit(1)
    
    while True:
        print("\nEmail Assistant Menu:")
        print("1. Generate and send an email")
        print("2. Generate email only")
        print("3. Configure email settings")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            to_email = input("Enter recipient email: ")
            prompt = get_multiline_input("\nEnter what you want the email to be about:")
            
            print("\nGenerating email...")
            subject, content = email_generator.generate_email(prompt)
            
            print("\n" + "="*50)
            print(f"Subject: {subject}")
            print("\n" + content)
            print("="*50)
            
            confirm = input("\nDo you want to send this email? (y/n): ")
            if confirm.lower() == 'y':
                success, message = email_sender.send_email(to_email, subject, content)
                print(message)
            else:
                print("Email sending canceled.")
        
        elif choice == '2':
            recipient = input("Enter recipient (optional, for context): ")
            prompt = get_multiline_input("\nEnter what you want the email to be about:")
            
            print("\nGenerating email...")
            subject, content = email_generator.generate_email(prompt, recipient=recipient)
            
            print("\n" + "="*50)
            print(f"Subject: {subject}")
            print("\n" + content)
            print("="*50)
            
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            print("\nCurrent email settings:")
            print(f"SMTP Server: {email_sender.smtp_server}")
            print(f"SMTP Port: {email_sender.smtp_port}")
            print(f"Email Address: {email_sender.email_address}")
            print("Email Password: [Hidden]")
            
            change = input("\nDo you want to change these settings? (y/n): ")
            if change.lower() == 'y':
                print("Please set the following environment variables in a .env file:")
                print("  SMTP_SERVER - Your email server")
                print("  SMTP_PORT - Your email server port")
                print("  EMAIL_ADDRESS - Your email address")
                print("  EMAIL_PASSWORD - Your email password")
                print("  MODEL_PATH - Path to your Llama model")
                input("\nPress Enter once you've set these variables...")
        
        elif choice == '4':
            print("Exiting Email Assistant. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")
        
        clear_screen()
        print_banner()

if __name__ == "__main__":
    main()