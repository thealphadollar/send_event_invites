from abc import ABC, abstractmethod
import csv
import re

EMAIL_REGEX = re.compile(r"\A[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
                         r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\z")


def protect(*protected):
    """
    Returns a metaclass that protects all attributes given as strings
    """

    class Protect(type):

        has_base = False

        def __new__(meta, name, bases, attrs):
            if meta.has_base:
                for attribute in attrs:
                    if attribute in protected:
                        raise AttributeError('Overriding of attribute "%s" not allowed.' % attribute)
            meta.has_base = True
            klass = super().__new__(meta, name, bases, attrs)
            return klass

    return Protect


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
            if label == "Email address":
                return row_index, col_index


class InsertEvent(ABC, metaclass=protect("read_csv", "create_event")):
    """
    An abstract base class to manage all the functions required to be accomplished to add an event.
    A new calendar AP can be easily added by creating another derived class and overriding the abstract methods.
    """

    # variables to store event and attendees' email addresses
    event = {}
    attendees = []

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

            print("reading CSV file...")
            csv_data = csv.reader(csv_file, delimiter=',')

            print("detecting row and column for email address...")
            skip_row_upto, email_index = find_email_index(csv_data)
            print("emails found in column {column_no} after row {row_no}".format(column_no=email_index,
                                                                                 row_no=skip_row_upto))

            print("adding emails...")
            discarded_addresses = []
            for row_index, row in enumerate(csv_data):
                if row_index > skip_row_upto:
                    if EMAIL_REGEX.match(row[email_index]):
                        self.attendees.append({'email': row[email_index]})
                    else:
                        discarded_addresses.append(row[email_index])

            print("the following E-mail address were rejected due to regex match failure \n",
                  "\n".join(discarded_addresses))

    def create_event(self, event_data):
        """
        Collects necessary event data from user, inserts more required parameters and adds it to self event.
        :param event_data: event data, provided in a dictionary format
        :return:
            None
        """
        print("appending additional necessary data to the event...")
        event_data.update(
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
                "guestsCanSeeOtherGuests": True
            }
        )
        self.event = event_data

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
