import argparse
from src.google_apis import create_service
import time
import tqdm 


parser = argparse.ArgumentParser()
parser.add_argument("--social_media",choices=["facebook","all"],default="facebook")
args = parser.parse_args()

def search_emails(service, query:str, user_id="me",):
    """
        Params:
        service
        query (str)  query to find specific emails
    """
    message_response = service.users().messages().list(
        userId = user_id,
        includeSpamTrash = False,
        q=query,
        maxResults=200
    ).execute()

    email_messages = message_response.get('messages')
    next_page_token = message_response.get('nextPageToken')
    time.sleep(0.5)
    return email_messages


def main():
    CLIENT_FILE="credentials.json"
    API_NAME = "gmail"
    API_VERSION ="v1"
    SCOPES = ["https://mail.google.com/"]
    
    gmail_service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

    if args.social_media == 'facebook':
        queries = ["from:reminders@facebookmail.com",
                    "from:friendsuggestion@facebookmail.com",
                    "from:friendupdates@facebookmail.com",
                    "from:notification@facebookmail.com"]




    for query in queries:
        email_results = search_emails(service=gmail_service,query=query)
        if email_results is None:
            continue
        for email_re in email_results:
            gmail_service.users().messages().trash(
                id=email_re["id"],
                userId="me"
            ).execute()
    return 0

if __name__ == "__main__":
    main()