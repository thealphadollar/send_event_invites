# Send Event Invites 

A  CLI tool for sending event invitations to a large number of attendees.

The tool has been made in such a manner that it is very easy to add new
calendar APIs and use them. 

## API support

Currently the client supports only Google Calendar.

## Get CSV file from Google Group

To export your Groups list into a .csv file:</br>
- Sign-in to Google Groups
- Click My Groups > check the name of the group
- In the upper right corner, click Manage
- Near the top right corner of the page, click Export Members

## Using the client

- To use the client, clone the repository.</br>
`git clone https://github.com/thealphadollar/send_event_invites`
- `cd send_event_invites`
- `pip install -r requirements.txt`
- `python3 src/main.py` if "attendees.csv" in src directory</br>
  `python3 src/main.py -p=[path_to_csv_file]` otherwise

## Accepted arguments

```text
Usage: main.py [OPTIONS]

  MEET MORE, LEARN MORE

  A CLI tool which sends email invites using the implemented API (currently
  GCalendar) to the address stored in attendees.csv or as path provided by
  --path param.

Options:
  --version                  Show the version and exit.
  --api [google]             API to use with the tool,
                             default is "google"
  -p, --path PATH            path to the csv file containing
                             email address of attendees, default is
                             "attendees.csv" in src directory
  -sd, --start-date TEXT     start date of the event, eg 2017-02-28 for
                             28 february 2017
  -st, --start-time TEXT     start time of the event. eg. 17:00
  -l, --location TEXT        location of the event
  -sum, --summary TEXT       summary of the event
  -ed, --end-date TEXT       end date of the event (same as start date, if not
                             provided), eg 2017-02-28 for 28 february 2017
  -et, --end-time TEXT       end time of the event. eg. 17:00
  -desc, --description TEXT  long description describing the event [optional]
  --help                     Show this message and exit.
```

## Contributing

Contributions to the project are welcome; a couple of very easy issues are present in the issue tab.

# Meet More, Learn More
