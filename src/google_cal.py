from insert_event import InsertEvent
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
import click

HOME_DIR = os.path.expanduser('~')
SCOPES = "https://www.googleapis.com/auth/calendar"
CLIENT_ID_FILE = ".client_id.json"
CREDENTIALS_FILE = os.path.join(HOME_DIR, ".cred_send_event_invite.json")
APPLICATION_NAME = "Send Event Invite"


class InsertEventGoogle(InsertEvent):

    service = None

    def auth(self):
        """
        Authorises the api using .client_id.json.
        :return:
            None
        """
        click.echo("google calendar authorisation initiated...")
        store = file.Storage(CREDENTIALS_FILE)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_ID_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store, None)
            click.echo("authorisation successful!\nstoring credentials in {address} for subsequent "
                       "use...".format(address=CREDENTIALS_FILE))
        else:
            click.echo("importing credentials from {address}...".format(address=CREDENTIALS_FILE))

        click.echo("building service...")
        self.service = build('calendar', 'v3', http=credentials.authorize(Http()))

    def insert(self):
        """
        Inserts the event in the google calendar.
        :return:
            None
        """
        click.echo("inserting event in owner's primary calendar...")
        created_event = self.service.events().insert(sendNotifications=True, calendarId='primary',
                                                     body=self.event_data).execute()
        click.echo("Voila! Event created:  {link}\n".format(
            link=created_event.get('htmlLink')
        ))
