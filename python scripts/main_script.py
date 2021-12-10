import weather_api as w_api
import calendar_api as c_api
import pandas as pd
import outfit_chooser as oc

database = pd.read_csv("..\Clothes_database.csv") # import clothing items database

def do_nothing():
    return None

def import_api_data():
    need_cold, need_wind, need_rain = w_api.weather_api()
    events = c_api.calendar_api(c_api.credentials)
    return need_cold,need_wind,need_rain,events

def get_keywords(events):
    keywords=list()
    for event in events:
        words = event.split(' ')
        for word in words:
            if(word == 'office' or word == 'casual' or word == 'party' or word == 'meeting' or word == 'hangout'):
                keywords.append(word)
    return keywords

def remove_classy():
    for i in range(len(database)):
        if (database.at[i,'Style'] == 'Casual' or database.at[i,'Style'] == 'Classy-casual'):
            database.drop(i,inplace=True)

    database.reset_index(drop=True, inplace=True)
    return None

def remove_casual():
    for i in range(len(database)):
        if (database.at[i,'Style'] == 'Classy'):
            database.drop(i,inplace=True)

    database.reset_index(drop=True, inplace=True)
    return None

def main():

    print('Hello and welcome to the Smart Closet v0.1! this is how the weather looks like:')

    need_cold,need_wind,need_rain,events = import_api_data()
    keywords = get_keywords(events)
    style = 'Casual'
    for elem in keywords:
        if(elem == 'party' and style != 'Classy'):
            style = 'Classy-casual'
        elif(elem == 'office' or elem == 'meeting'):
            style = 'Classy'
    
    style = input('The style for today will be: ' + style + '.\nIf you would prefer another style, please specify(Casual/Classy-casual/Classy):')
    print('Please stand by while we choose your outfit for you.\n')

    match(style):
        case 'Casual':
            remove_casual()
        case 'Classy-casual':
            do_nothing()
        case 'Classy':
            remove_classy()
        case _:
            do_nothing()
    
    outfit = oc.Outfit(need_cold,need_wind,need_rain,style,database)

if __name__ == "__main__":
    main()