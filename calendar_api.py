# Application (client) ID: 9568e72e-9eb7-4bcb-a14e-72ba6a477539
# Secret ID value: dc59a1ac-f819-47be-9dd1-470805953ad7
# Secret key value: nr~7Q~aMcqDhl5RuHPoJyBqhbFC6y3WPcUln5

from O365 import Account, MSGraphProtocol
import datetime as dt

CLIENT_ID = '9568e72e-9eb7-4bcb-a14e-72ba6a477539'
SECRET_ID = 'nr~7Q~aMcqDhl5RuHPoJyBqhbFC6y3WPcUln5'
credentials = (CLIENT_ID, SECRET_ID)

def calendar_api(credentials):

   protocol = MSGraphProtocol() 
   #protocol = MSGraphProtocol(defualt_resource='<sharedcalendar@domain.com>') 
   scopes = ['Calendars.Read']
   account = Account(credentials, protocol=protocol)

   if account.authenticate(scopes=scopes):
      print('Authenticated!')

   schedule = account.schedule()
   calendar = schedule.get_default_calendar()

   q = calendar.new_query('start').greater_equal(dt.date.today())

   #ev = calendar.get_events(include_recurring=False) 
   ev = calendar.get_events(query=q, include_recurring=False) 

   events=list()

   for event in ev:
      ev_str= str(event)
      end_index= ev_str.find('(')-1
      events.append(ev_str[9:end_index])
   
   return events
