from abc import ABC, abstractmethod
import csv
import re
import click

email_exp = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)" \
            "+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
EMAIL_REGEX = re.compile(email_exp)


def find_email_index(csv_data):
    """
    Returns the column index for a row at which email address is stored.
    :param csv_data: data extracted by csv
    :return:
        row_index: index till which labels are there, used to skip to data
        col_index: index of the email address column
    """
    for row_index, row in enumerate(csv_data):
        for col_index, label in enumerate(row):
            if str(label).lower() == "email address":
                return row_index, col_index


class InsertEvent(ABC):
    """
    An abstract base class to manage all the functions required to be accomplished to add an event.
    A new calendar AP can be easily added by creating another derived class and overriding the abstract methods.
    """

    # variables to store event and attendees' email addresses
    event_data = {}
    attendees = []
    discarded_addresses = []

    def add_event_data(self, start_date, start_time, location, summary, end_date, end_time, description):
        click.echo("adding details to the event...")
        self.event_data = {
            'summary': summary,
            'location': location,
            'start':
                {
                    'dateTime': str(start_date + "T" + start_time + ":00"),
                    'timeZone': 'Asia/Kolkata'
                }
        }

        if end_date is not None:
            self.event_data.update(
                {
                    'end':
                        {
                            'dateTime': str(end_date + "T" + "00:00:00"),
                            'timeZone': 'Asia/Kolkata'
                        }
                }
            )
        else:
            self.event_data.update(
                {
                    'end':
                        {
                            'dateTime': str(start_date + "T" + end_time + ":00"),
                            'timeZone': 'Asia/Kolkata'
                        }
                }
            )

        if description is not None:
            self.event_data.update(
                {
                    'description': description
                }
            )

    def read_csv(self, file_path):
        """
        Reads a csv file and appends the email addresses of attendees to attendees.
        Currently compatible with any csv file having parameter "Email address" as topic above addresses.
        The method performs a regex check and discards wrongly formatted email addresses.
        :param file_path: path to csv file (default is "./addresses.csv")
        :return:
            Appends the email addresses to the attendees list
        """

        with open(file_path) as csv_file:

            click.echo("reading {path} file...".format(path=file_path))
            csv_data = csv.reader(csv_file, delimiter=',')

            click.echo("detecting row and column for email address...")
            skip_row_upto, email_index = find_email_index(csv_data)
            click.echo("emails found in column {column_no} after row {row_no}".format(column_no=email_index,
                                                                                      row_no=skip_row_upto))

            click.echo("adding emails...")
            for row_index, row in enumerate(csv_data):
                if EMAIL_REGEX.match(str(row[email_index]).lower()):
                    self.attendees.append({'email': row[email_index]})
                else:
                    self.discarded_addresses.append(row[email_index])

    def create_event(self):
        """
        Inserts more required parameters to self.event_data
        :return:
            None
        """
        click.echo("appending additional necessary data to the event...")
        self.event_data.update(
            {
                "attendees": self.attendees,
                "reminders":
                    {
                        "useDefault": False,
                        "overrides":
                        [
                            {"method": "email", "minutes": 24 * 60},
                            {"method": "email", "minutes": 6 * 60},
                            {"method": "popup", "minutes": 60}
                        ]
                    },
                "guestsCanInviteOthers": True,
                "guestsCanSeeOtherGuests": True,
                "sendNotifications": True
            }
        )

    @abstractmethod
    def auth(self):
        """
        Facilitates authentication for the API.
        :return:
            None
        """
        # To be implemented in the derived class.
        pass

    @abstractmethod
    def insert(self):
        """
        Uploads the event using the api to the calendar.
        :return:
            None
        """
        # To be implemented in the derived class.
        pass

    def display_discarded(self):
        """
        displays list of email addresses that did not match the REGEX
        :return:
            None
        """
        if len(self.discarded_addresses) > 0:
            click.echo("The following inputs were rejected due to not matching Email Address format,")
            click.echo(self.discarded_addresses)
