import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonButton, IonRow, IonCard, IonCardHeader, IonCardContent} from '@ionic/react';
import ExploreContainer from '../components/ExploreContainer';
import './Tab2.css';

const Tab2: React.FC = () => {
  const weather = {
    fetchWeather: () => {
      let url = 'https://api.openweathermap.org/data/2.5/onecall?lat=51.4792547&lon=5.6570096&exclude=minutely,daily,alerts&appid=a1e792276ae4a0741f8a93ce2377dd94&units=metric'
      fetch(url)
        .then(resp=>{
          if(!resp.ok) throw new Error(resp.statusText);
          return resp.json();
        })
        .then(data=>{
          weather.showWeather(data);
        })
        .catch(console.error);
        
    },
    showWeather: (resp: any) => {
      let cur = resp.current;
      console.log(cur);
      return {
        cur
      }
    }
  };
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Tab 2</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent>
        <IonButton onClick={weather.fetchWeather}>
          Get weather
        </IonButton>
      </IonContent>
      <IonRow >

      </IonRow>
    </IonPage>
  );
};

export default Tab2;