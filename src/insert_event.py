from abc import ABC, abstractmethod
import csv


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
            csv_data = csv.reader(csv_file, delimiter=',')
            skip_row_upto, email_index = find_email_index(csv_data)

            for row_index, row in enumerate(csv_data):
                if row_index > skip_row_upto:
                    self.attendees.append(row[email_index])

    def create_event(self, event_data):
        """
        Collects event data and adds it to the event dictionary.
        :param event_data: event data, provided in a list format
        :return:
            None
        """
        pass

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
