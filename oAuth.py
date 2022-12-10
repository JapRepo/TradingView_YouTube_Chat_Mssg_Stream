import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials



def Authenticate(tokenOld,client_id):
    creds = None
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_info(tokenOld, scopes)
        
    # If there are no valid credentials available, then either refresh the token or log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json',
                    scopes = scopes
                )

            flow.run_local_server(port=8080, prompt='consent',authorization_prompt_message='')
            creds = flow.credentials

        # Save the credentials for the next run
    return creds