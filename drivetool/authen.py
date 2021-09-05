from __future__ import print_function
import pickle
import os
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#If modify SCOPES, please delete the file: token.pickle
SCOPES = ['https://www.googleapis.com/auth/drive.metadata',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file'
          ]


def get_gdrive_service(cred_file: str):
    """The file token.pickle stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    """

    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(cred_file), SCOPES)
                creds = flow.run_local_server(port=8080)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        except:
            print("//error: API authentication hasn't done yet or with wrong credential file")
            print("please initialize with auth command again")
            sys.exit()

    return build('drive', 'v3', credentials=creds)


def init_auth(args):
    """Initialize Api authentication data
    """
    
    cred_file = args.credentials

    if os.path.exists('token.pickle'):
        try:
            os.remove('token.pickle')
        except OSError as e:
            print(e)

    service = get_gdrive_service(cred_file)
    print("API authentication succeeds")