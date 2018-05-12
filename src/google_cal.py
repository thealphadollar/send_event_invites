from insert_event import InsertEvent
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
import click

home_dir = os.path.expanduser('~')


class InsertEventGoogle(InsertEvent):

    service = None

    def auth(self):
        """
        Authorises the api using .client_id.json.
        :return:
            None
        """
        click.echo("google calendar authorisation initiated...")
        scope = "https://www.googleapis.com/auth/calendar"
        store = file.Storage(os.path.join(home_dir, '.credentials.json'))
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets('.client_id.json', scope)
            credentials = tools.run_flow(flow, store)
        click.echo("authorisation successful!\nbuilding service...")
        self.service = build('calendar', 'v3', http=credentials.authorize(Http()))

    def insert(self):
        """
        Inserts the event in the google calendar.
        :return:
            None
        """
        click.echo("inserting event in owner's primary calendar...")
        created_event = self.service.events().insert(calendarId='primary', body=self.event_data,
                                                     sendNotifications=True).execute()
        click.echo("Voila! Event created:  {link}\nHangouts link: {hang_link}".format(
            link=created_event.get('htmlLink'),
            hang_link=created_event.get('hangoutLink')
        ))
