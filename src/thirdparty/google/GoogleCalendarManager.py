import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta, timezone
from typing import List, Dict
from dotenv import load_dotenv
from src.common.util.log import LogHandler
from src.parsers.GoogleCalenderEventParser import Operation

logger = LogHandler().get_logger()

load_dotenv()

class GoogleCalendarManager:

    SCOPES = ['https://www.googleapis.com/auth/calendar']


    def __init__(self):
        self.credentials_path = os.getenv("CREDENTIALS_PATH")
        self.token_path = os.getenv("TOKEN_PATH")
        self.service = self.get_calendar_service()

    def get_calendar_service(self):
        creds = self.authenticate()
        service = build('calendar', 'v3', credentials=creds)
        return service

    def authenticate(self):
        # Authenticate and create Google Calendar service
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)  # Path to your credentials file
                creds = flow.run_local_server(port=0)
                logger.debug(f"Authorized Scopes: {creds.scopes}")
            # Save the credentials for the next run
            with open(self.token_path, 'wb') as token:
                token.write(creds.to_json().encode('utf-8'))  # Encode the string to bytes

        return creds

    def find_duplicate_events(self, summary: str, start_time: str) -> List[dict]:
        """Find events with the same name and similar start time"""
        try:
            # Convert start time to datetime and create a time range
            #start = datetime.fromisoformat(start_time)
            #time_min = (start - timedelta(hours=24)).isoformat() + 'Z'
            #time_max = (start + timedelta(hours=48)).isoformat() + 'Z'

            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))  # Handles 'Z' or offset
            start_utc = start_dt.astimezone(timezone.utc)  # Convert to UTC
            time_min = (start_utc - timedelta(hours=24)).isoformat().replace('+00:00', 'Z')
            time_max = (start_utc + timedelta(hours=48)).isoformat().replace('+00:00', 'Z')

            # Find events with the same name and similar start time using the service
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                q=summary,
                singleEvents=True
            ).execute()
            return events_result.get('items', [])
        except Exception as e:
            logger.error(f"Error finding duplicate events: {e}")
            return []

    def create_event(self, summary: str, description: str, start_time: str, end_time: str) -> str:
        """Create a new calendar event with duplicate handling"""
        # Check for duplicate events
        duplicates = self.find_duplicate_events(summary, start_time)

        if duplicates:
            # Option to handle duplicates: append a number or modify
            summary = f"{summary} (Copy {len(duplicates) + 1})"

        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))  # Handles 'Z' or offset
        start_utc = start_dt.astimezone(timezone.utc).isoformat()  # Convert to UTC
        end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))  # Handles 'Z' or offset
        end_utc = end_dt.astimezone(timezone.utc).isoformat()  # Convert to UTC

        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_utc,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_utc,
                'timeZone': 'UTC',
            },
        }

        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            return {
                'status': 'success',
                'message': f"{str(event)}"
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error creating event: {str(e)}"
            }

    def delete_event(self, event_id: str) -> Dict:
        """
        Delete an event by its ID

        :param event_id: ID of the event to delete
        :return: Deletion status
        """
        try:
            # Verify event exists before deletion
            self.service.events().get(
                calendarId='primary',
                eventId=event_id
            ).execute()

            # Delete the event
            self.service.events().delete(
                calendarId='primary',
                eventId=event_id
            ).execute()

            return {
                'status': 'success',
                'message': 'Event deleted successfully'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to delete event: {str(e)}"
            }

    def update_event(self, event_id: str, updates: dict) -> str:
        """Update an existing event"""
        try:
            # Fetch the existing event first
            event = self.service.events().get(calendarId='primary', eventId=event_id).execute()

            # Apply updates
            event.update(updates)

            # Update the event
            updated_event = self.service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event
            ).execute()

            #return f"Event updated: {updated_event.get('htmlLink')}"
            return updated_event
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error updating event: {str(e)}"
            }

    def list_events(self,max_results=10):
        now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        logger.debug('Getting the upcoming events')
        events_result = self.service.events().list(calendarId='primary',  # 'primary' is your default calendar
                                              timeMin=now,
                                              maxResults=max_results,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            logger.debug('No upcoming events found.')
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            logger.info(start, event['summary'])

    def performOperation(self, response) -> Dict:

        calendar_manager = GoogleCalendarManager()

        # Determine the operation type and call the respective function
        operation = response['event'].get('operation')
        event_details = response['event']

        if operation == Operation.CREATE:
            return calendar_manager.create_event(
                summary=event_details['summary'],
                description=event_details.get('description', ''),
                start_time=event_details['start_time'],
                end_time=event_details['end_time']
            )
        elif operation == Operation.UPDATE:
            return calendar_manager.update_event(
                event_id=event_details['event_id'],
                updates=event_details['updates']
            )
        elif operation == Operation.DELETE:
            return calendar_manager.delete_event(event_id=event_details['event_id'])
        elif operation == Operation.RETRIEVE:
            return calendar_manager.list_events(max_results=event_details.get('max_results', 10))
        else:
            return  {"status": "error", "message": "Invalid operation type"}
'''
#def main():
#    calenderservice = GoogleCalendarManager()
    #service = calenderservice.service

    # Example Usage:
    #calenderservice.list_events()

#    start_time = '2025-02-11T10:00:00+05:30'
#    end_time = '2025-02-11T11:00:00+05:30'
#    new_event = calenderservice.create_event( 'New New Scrum - please delete all else - MindMentors','Discuss project updates', start_time, end_time )

#    print(new_event)
    # Update the event
    #create a dictionary with the updates
#    updates = {
#        'summary': 'Updated Meeting Title',
#        'description': 'New description'
#    }
#    #calenderservice.update_event( new_event['id'], updates)

#    calenderservice.delete_event(new_event['id'])

#if __name__ == '__main__':
#    main()

'''

