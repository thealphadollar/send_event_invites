from abc import ABC, abstractmethod


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
                        raise AttributeError('Overriding of attribute "%s" not allowed.'%attribute)
            meta.has_base = True
            klass = super().__new__(meta, name, bases, attrs)
            return klass

    return Protect


class InsertEvent(ABC, metaclass=protect("read_csv", "create_event")):
    """
    An abstract base class to manage all the functions required to be accomplished to add an event.
    A new calendar AP can be easily added by creating another derived class and overriding the abstract methods.
    """

    # variable to store event
    event = {}
    attendees = []

    def read_csv(self, file_path):
        """
        Reads a csv file and appends the email addresses of attendees to attendees.
        The method performs a regex check and discards wrongly formatted email addresses.
        :param file_path: path to csv file (default is "./addresses.csv")
        :return:
            Appends the email addresses to the attendees list
        """
        pass

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
        pass

    @abstractmethod
    def insert(self):
        """
        Uploads the event using the api to the calendar.
        :return:
            None
        """
        pass
