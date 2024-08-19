import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
from googleapiclient.discovery import build

"""
This is verified to be working on 19/08/2024.

Enable the google APIs for your account from console,cloud.google.com
Get the OAuth 2.0 JSON, and enable the google sheets API and add the needed scopes. 
Assuming that the above has been done:
Create your App script.
Click on Deploy
click on New Deployment
Select type - API executable (change project type if needed in the google console) 
When deployed, get the deployment ID. Example - *************************-Bu06H98jJM2cmiOXekCpEyUwUd9cy1Bbzi4z-*********
Put the ID in the variable "deployment_id"
Change the function name in the request
Run
"""

# Define the scopes that your application needs access to. These scopes are used to request permission
# to access specific resources (e.g., Google Sheets, Google Script, etc.)
SCOPES = ['https://www.googleapis.com/auth/script.projects',
          'https://www.googleapis.com/auth/script.scriptapp',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/spreadsheets.currentonly']


def google_script_trigger():
    creds = None

    # Check if the token.json file exists, which stores your access and refresh tokens.
    # If it exists, load the credentials from the file.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If credentials are not available or are invalid (e.g., expired), refresh or obtain new credentials.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh the credentials if they have expired.
            creds.refresh(Request())
        else:
            # If there are no credentials or they cannot be refreshed, initiate the OAuth2 flow to get new credentials.
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json',
                scopes=SCOPES
            )
            # Run the local server to get user authorization and generate new credentials.
            creds = flow.run_local_server(port=8000)
        # Save the new credentials for future use in the token.json file.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Build the Google Apps Script API service with the obtained credentials.
        service = build('script', 'v1', credentials=creds)

        # The deployment ID of the Google Apps Script project to be executed.
        deployment_id = '' 

        # The request payload that contains the function name to be executed in the Apps Script
        # and any parameters required by that function.
        request = {
            'function': 'changeColor',  # Function name to execute. Change to your Apps Script function
            'parameters': [],  # If parameters are needed to pass to the function, include them here.
        }

        # Execute the script function using the built service and deployment ID.
        response = service.scripts().run(body=request, scriptId=deployment_id).execute()

        # Print the response from the script execution.
        print(response)
    except errors.HttpError as error:
        # Handle any errors that occur during the script execution.
        print(error.content)


google_script_trigger()
