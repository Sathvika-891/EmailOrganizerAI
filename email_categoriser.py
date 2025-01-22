import os.path
import base64
import os
import pandas as pd
from email import message_from_bytes
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from litellm import completion
from tqdm import tqdm
os.environ["GROQ_API_KEY"]=""

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

CATEGORIES = [
    "Work",
    "Personal",
    "Finance",
    "Shopping",
    "Social",
    "Newsletters"
]

def get_gmail_service():
    """Gets authenticated Gmail service."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return build("gmail", "v1", credentials=creds)

def get_email_content(service, message_id):
    """Retrieves email content for a given message ID."""
    try:
        message = service.users().messages().get(userId='me', id=message_id, format='raw').execute()
        msg_bytes = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        email_message = message_from_bytes(msg_bytes)
        
        subject = ''
        if 'subject' in email_message:
            subject = email_message['subject']
        
        body = ''
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()
        
        return {
            'subject': subject,
            'body': body[:1000]  # Limit body length to avoid token limits
        }
    except Exception as e:
        print(f"Error getting email content: {e}")
        return {'subject': '', 'body': ''}

def classify_email(email_content):
    """Classifies email using OpenAI API."""
    prompt = f"""Please classify the following email into exactly one of these categories: {', '.join(CATEGORIES)}.
    Respond with just the category name, nothing else.
    
    Email Subject: {email_content['subject']}
    Email Body: {email_content['body']}
    """
    
    try:
        response = completion(
            model="groq/llama3-8b-8192", 
            messages=[
            {"role": "system", "content": "You are an email classifier. Respond only with the category name."},
            {"role": "user", "content": prompt}
        ],
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error classifying email: {e}")
        return "Unknown"

def main():
    """Main function to classify emails."""
    try:
        print("Initializing Gmail service...")
        service = get_gmail_service()
        
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print("No emails found.")
            return
        
        # Create a list to store results
        email_data = []
        
        # Process emails with a single progress bar
        for message in tqdm(messages, desc="Processing emails"):
            email_content = get_email_content(service, message['id'])
            category = classify_email(email_content)
            
            # Append to email_data list
            email_data.append({
                'message_id': message['id'],
                'subject': email_content['subject'],
                'content': email_content['body'],
                'category': category
            })
        
        # Convert to DataFrame and save to CSV
        df = pd.DataFrame(email_data)
        df.to_csv('results.csv', index=False)
        print(f"\nResults saved to results.csv")
        
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
