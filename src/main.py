from google_cal import InsertEventGoogle
import click
from . import __version__


def set_api(name):
    """
    Sets the API for the calendar.
    Currently supported: Google Calendar.
    :param name:
            google: sets Google Calendar as API
    :return:
        cal_api:
            an instance of the chosen API
    """
    pass


# TODO: Add click commands
def main():  # TODO: Add required parameters
    pass


if __name__ == '__main__':
    main()
