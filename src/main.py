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
    if name == "google":
        return InsertEventGoogle()


@click.command()
@click.version_option(version=__version__, prog_name="send_event_invite")
@click.option('--api', default="google", type=click.Choice(['google']))
@click.option('--path', '-p', default="attendees.csv", type=click.Path(exists=True), help="path to the csv file \
                containing email address of attendees, default is \"attendees.csv\" in current directory")
@click.option('--start-date', prompt="start date [yyyy-mm-dd]", help="start date of the event, eg 2017-02-28 for\
                                                                           28 february 2017")
@click.option('--start-time', prompt="start time [hrs:mns]", help="start time of the event. eg. 17:00")
@click.option('--location', prompt="location", help="location of the event")
@click.option('--summary', prompt="summary", help="summary of the event")
@click.option('--end-date', default=None, help="end date of the event, eg 2017-02-28 for 28 february 2017")
@click.option('--end-time', default=None, help="start time of the event. eg. 17:00")
@click.option('--description', default=None, help="long description describing the event")
def main(api, path, start_date, start_time, location, summary, end_date, end_time, description):
    """
    A CLI tool which sends email invites using the implemented API (currently GCalendar) to the
    address stored in attendees.csv or as path provided by --path param.
    """
    event_handler = set_api(api)
    event_handler.add_event_data(start_date, start_time, location, summary, end_date, end_time, description)
    event_handler.read_csv(path)
    event_handler.create_event()
    event_handler.auth()
    event_handler.insert()
    event_handler.display_discarded()


if __name__ == '__main__':
    main()
