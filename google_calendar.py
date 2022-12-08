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


def total(client_name: list, client_description: list, client_date: list, client_time: list):
    # ['2023', '01', '26'] ['15'] - > '2023-01-26T15:00:00' | for google calendar API
    date_cal = f'{client_date[0]}-{client_date[1]}-{client_date[2]}T{client_time[0]}:00:00'

    # Add event
    event = {
        'summary': f'{client_name[0]}, {client_name[1]}',
        'description': f'{client_description}',
        'start': {
            'dateTime': date_cal,
            'timeZone': 'Europe/Berlin',
        },
        'end': {
            'dateTime': date_cal.replace(':00', ':40'),
            'timeZone': 'Europe/Berlin',
        },
    }
    obj.add_event(calendar_id=name_calendar_id, body=event)


def get_calendar_data(name):
    event = obj.service.events().list(calendarId=name_calendar_id).execute()  # get data from all event
    info = []  # create to collect info from user entry
    how_many = range(len(event['items']))  # how many entry has user
    for i in how_many:
        if event['items'][i]['summary'] == name:  # if name of user in calendar event
            info.append(f"Дата : {event['items'][i]['start']['dateTime'][:10]}\n" \
                        f"Время : {event['items'][i]['start']['dateTime'][11:13]}:00\n\n")
        else:  # if user has not event in google calendar
            info.append('У вас нет записей\nЕсли вы уверены что записывались\nто нажмите сюда 👉 /help')
    return how_many, info  # how_many -> int


# obj.service.events().delete(calendarId=name_calendar_id, eventId='lmoa6q24cgnr9n87cp4rv790uo').execute()
