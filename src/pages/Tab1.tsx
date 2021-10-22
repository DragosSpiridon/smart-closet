import * as mobiscroll from '@mobiscroll/react';
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import ExploreContainer from '../components/ExploreContainer';
import React from 'react';
import { Eventcalendar, getJson, toast, MbscCalendarEvent, MbscEventcalendarView } from '@mobiscroll/react';
import './Tab1.css';


const Tab1: React.FC = () => {
  
  const [myEvents, setEvents] = React.useState<MbscCalendarEvent[]>([]);

    React.useEffect(() => {
        getJson('https://trial.mobiscroll.com/events/?vers=5', (events: MbscCalendarEvent[]) => {
            setEvents(events);
        }, 'jsonp');
    }, []);

    const onEventClick = React.useCallback((event) => {
        toast({
            message: event.event.title
        });
    }, []);

    const view = React.useMemo<MbscEventcalendarView>(() => {
        return {
            calendar: { type: 'week' },
            agenda: { type: 'day' }
        };
    }, []);

    return (
        <Eventcalendar
            theme="ios" 
            themeVariant="light"
            data={myEvents}
            view={view}
            onEventClick={onEventClick}
        />
    );
  
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Tab 1</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">Tab 1</IonTitle>
          </IonToolbar>
        </IonHeader>
        <ExploreContainer name="Tab 1 page" />
      </IonContent>
    </IonPage>
  );
};

export default Tab1;


/*

import React from 'react';
import '@mobiscroll/react/dist/css/mobiscroll.min.css';
import { Eventcalendar, getJson, toast, MbscCalendarEvent, MbscEventcalendarView } from '@mobiscroll/react';

const App: React.FC = () => {

    const [myEvents, setEvents] = React.useState<MbscCalendarEvent[]>([]);

    React.useEffect(() => {
        getJson('https://trial.mobiscroll.com/events/?vers=5', (events: MbscCalendarEvent[]) => {
            setEvents(events);
        }, 'jsonp');
    }, []);

    const onEventClick = React.useCallback((event) => {
        toast({
            message: event.event.title
        });
    }, []);

    const view = React.useMemo<MbscEventcalendarView>(() => {
        return {
            calendar: { type: 'week' },
            agenda: { type: 'day' }
        };
    }, []);

    return (
        <Eventcalendar
            theme="ios" 
            themeVariant="light"
            data={myEvents}
            view={view}
            onEventClick={onEventClick}
        />
    );
}

*/