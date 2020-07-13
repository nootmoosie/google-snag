from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)

  service = build('drive', 'v3', credentials=creds)

  # Call the Drive v3 API
  service.files()

  # "webContentLink": "A String", # A link for downloading the content of the file in a browser. This is only available for files with binary content in Google Drive.
  results = service.files().list(
    fields="nextPageToken, files(id, name, capabilities)").execute()
  items = results.get('files', [])

  if not items:
    print('No files found.')
  else:
    print('Files:')
    for item in items:
      # download: int = item['capabilities'] 
      download = item['capabilities'].get("canDownload")
      print(u'attempt download of {0} ~~~~ access: {1}'.format(item['name'], download))
      print(u'{0} ({1}) download: {2}'.format(item['name'], item['id'], download))

if __name__ == '__main__':
  main()
