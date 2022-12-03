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


def total(client_time, client_description, client_name):
    total_time = ''
    for x in client_time:
        total_time += x
    total_name = ''
    total_description = ''

    for i in client_description:
        total_description += f'{i}, '

    for i in client_name:
        total_name += f'{i}, '

    # Add event
    event = {
        'summary': total_name,
        'description': total_description,
        'start': {
            'dateTime': total_time,
            'timeZone': 'Europe/Berlin',
        },
        'end': {
            'dateTime': total_time.replace('14:00', '14:40'),
            'timeZone': 'Europe/Berlin',
        },
    }
    obj.add_event(calendar_id=name_calendar_id, body=event)

