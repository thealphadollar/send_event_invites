from google_cal import InsertEventGoogle
from __init__ import __version__
import click


def set_api(name):
    """
    Sets the API for the calendar.
    Currently supported: Google Calendar.
    :param name:
            google: sets Google Calendar as API
    :return:
            an instance of the chosen API
    """
    if name == "google":
        return InsertEventGoogle()


@click.command()
@click.version_option(version=__version__, prog_name="send_event_invite")
@click.option('--api', default="google", type=click.Choice(['google']), help="API to use with the tool, \
                                                                                    default is \"google\"")
@click.option('--path', '-p', default="attendees.csv", type=click.Path(exists=True), help="path to the csv file \
                containing email address of attendees, default is \"attendees.csv\" in current directory")
@click.option('--start-date', '-sd', prompt="Start Date [yyyy-mm-dd]", help="start date of the event, eg 2017-02-28 for\
                                                                           28 february 2017")
@click.option('--start-time', '-st', prompt="Start Time [hrs:mns]", help="start time of the event. eg. 17:00")
@click.option('--location', '-l', prompt="Location", help="location of the event")
@click.option('--summary', '-sum', prompt="Summary", help="summary of the event")
@click.option('--end-date', '-ed', default=None, help="end date of the event (same as start date, if not provided), "
                                                      "eg 2017-02-28 for 28 february 2017")
@click.option('--end-time', '-et', prompt="End Time [hrs:mns]", help="end time of the event. eg. 17:00")
@click.option('--description', '-desc', prompt="Description", help="long description describing the event [optional]")
def main(api, path, start_date, start_time, location, summary, end_date, end_time, description):
    """
    A CLI tool which sends email invites using the implemented API (currently GCalendar) to the
    address stored in attendees.csv or as path provided by --path param.
    """

    if len(description) == 0:
        description = None

    event_handler = set_api(api)
    event_handler.add_event_data(start_date, start_time, location, summary, end_date, end_time, description)
    event_handler.read_csv(path)
    event_handler.create_event()
    event_handler.auth()
    event_handler.insert()
    event_handler.display_discarded()


if __name__ == '__main__':
    main()
