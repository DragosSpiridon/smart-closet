import weather_api as w_api
import calendar_api as c_api
import pandas as pd
import outfit_chooser as oc
import os
import streamlit as st

database = pd.read_csv(os.path.dirname(__file__) + '/../Clothes_database.csv') # import clothing items database
if 'first_time' not in st.session_state:
    st.session_state.first_time = True


def do_nothing():
    return None

def import_api_data():
    need_cold, need_wind, need_rain, temp, wind, weather = w_api.weather_api()
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
    st.write("""
    # Smart Closet v0.3
    ### Good day, user! Keep an eye on the terminal and follow its instructions when appropriate.
    """)
    need_cold,need_wind,need_rain,temp, wind, weather = w_api.weather_api()
    #st.write('The weather right now is ', weather, '.')
    #st.write('The average temperature over the next 6 hours is ', temp, ' degrees Celsius.')
    #st.write('The average wind speed over the next 6 hours  is ', wind, ' m/s.')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write("""
        ##### Weather:
        """,weather)
    with col2:
        limited_temp = round(temp,2)
        string_temp = "%a °C"%str(limited_temp)
        st.metric(label="Temperature", value=string_temp)
    with col3:
        limited_wind = round(wind,2)
        string_wind = "%a m/s"%str(limited_wind)
        st.metric(label="Wind speed", value=string_wind)

    if st.session_state.first_time:
        events = c_api.calendar_api(c_api.credentials)
        st.session_state.first_time = False
        if 'keywords' not in st.session_state:
            st.session_state.keywords = get_keywords(events)

    style = 'Casual'
    for elem in st.session_state.keywords:
        if(elem == 'party' and style != 'Classy'):
            style = 'Classy-casual'
        elif(elem == 'office' or elem == 'meeting'):
            style = 'Classy'
    
    st.write('#### The style for today will be ', style,'. If you would like to change this, choose it from the list below.')
    
    user_style = st.radio('Style', ('Casual', 'Classy-casual', 'Classy'))
    if not user_style:
        st.warning('Please select a style.')
        st.stop()
    else:
        style = user_style
    
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

    
    st.button('Choose another outfit', on_click = outfit.choose_outfit())
    
    
    items = list()

    if (outfit.coat != None):
        items.append(outfit.coat)
    if (outfit.top2 != None):
        items.append(outfit.top2)
    items.append(outfit.top1)
    items.append(outfit.bottom)
    items.append(outfit.footwear)
    st.dataframe(database.iloc[items])

    with st.expander("Change outfit elements"):
        with st.form("Outfit items"):
            options = st.multiselect('Which items do you wish to change?',database.iloc[items])
            st.write('You selected:', options)
            print(options)
            submitted = st.form_submit_button("Change")
            if submitted:
                st.write("Outfit was changed to:")
                st.dataframe(database.iloc[items])


if __name__ == "__main__":
    main()