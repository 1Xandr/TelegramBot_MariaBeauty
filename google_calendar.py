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


# create event in google calendar
def total(client_name: list, client_description: list, client_date: list, client_time: list):
    # ['2023', '01', '26'] ['15'] - > '2023-01-26T15:00:00' | for google calendar API
    date_cal = f'{"-".join(client_date)}T{client_time[0]}:00:00'

    # Add event
    event = {
        'summary': ', '.join(client_name),  # ['Alex', '123'] -> 'Alex, 123'
        'description': ''.join(client_description),  # ['Депиляция', 'Бикини'] -> Депиляция, Бикини
        'start': {
            'dateTime': date_cal,  # '2023-01-26T15:00:00'
            'timeZone': 'Europe/Berlin',
        },
        'end': {
            'dateTime': date_cal.replace(':00', ':40'),  # '2023-01-26T15:00:00' ->  '2023-01-26T15:40:00'
            'timeZone': 'Europe/Berlin',
        },
    }
    obj.add_event(calendar_id=name_calendar_id, body=event)  # add event into google calendar


# get entry of client
def get_calendar_data(name: str):
    event = obj.service.events().list(calendarId=name_calendar_id).execute()  # get data from all event
    info = []  # create to collect info from user entry
    title = []  # create for text of button
    event_id = []  # collect eventID for (delete_event)
    date_for_sql = []
    how_many = range(len(event['items']))  # how many entry has user
    for i in how_many:
        if event['items'][i]['summary'] == name:  # if name of user in calendar event

            # for my_entry:delete
            date = f"{event['items'][i]['start']['dateTime'][:10]} "  # 2022-12-11
            time = f" {event['items'][i]['start']['dateTime'][11:13]}:00"  # 14:00
            title.append('Удалить запись: ' + date + time)  # Удалить запись: 2022-12-11 | 14:00
            event_id.append(event['items'][i]['id'])  # append eventID

            # 2022-12-11T15:00:00+01:00 -> '"2022-12-11"' | 'T15'
            date_for_sql.append(f"{event['items'][1]['start']['dateTime'][:10]}")  # add date
            date_for_sql.append(f"T{event['items'][1]['start']['dateTime'][11:13]}")  # add time

            # for my_entry:my
            info.append(f"<b>Дата</b> : <u>{date}</u>\n"
                        f"<b>Время</b> : <u>{time}</u>\n"
                        f"<b>Услуга</b> :\n🤍 <b>{event['items'][i]['description']}</b>\n"
                        f"----------------------------------------\n")

    return how_many, info, title, event_id, date_for_sql


def delete_event(event_id: str):  # delete event
    obj.service.events().delete(calendarId=name_calendar_id, eventId=event_id).execute()
