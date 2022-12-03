from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    FILE_PATH = 'xandr-1-cf9958cace58.json'

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            filename=self.FILE_PATH, scopes=self.SCOPES
        )
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self, calendar_id):
        calendar_list_entry = {
            'id': calendar_id
        }
        return self.service.calendarList().insert(body=calendar_list_entry).execute()

    def add_event(self, calendar_id, body):
        return self.service.events().insert(calendarId=calendar_id, body=body).execute()


obj = GoogleCalendar()
name_calendar_id = 'sashacaha2019@gmail.com'


def total(client_date, client_description, client_name):
    total_name = ''
    total_description = ''
    time_cal = f'{client_date[0]}{client_date[1]}{client_date[2]}'
    for i in client_description:
        total_description += f'{i}, '

    for i in client_name:
        total_name += f'{i}, '

    # Add event
    event = {
        'summary': total_name,
        'description': total_description,
        'start': {
            'dateTime': time_cal,
            'timeZone': 'Europe/Berlin',
        },
        'end': {
            'dateTime': time_cal.replace(':00', ':40'),
            'timeZone': 'Europe/Berlin',
        },
    }
    obj.add_event(calendar_id=name_calendar_id, body=event)

