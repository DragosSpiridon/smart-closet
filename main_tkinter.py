import weather_api as w_api
import calendar_api as c_api
import outfit_chooser as oc
from tkinter import *
from tkinter import messagebox, ttk
import pandas as pd

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

def update_table():
    db_view.delete(*db_view.get_children())
    user_style = radioStyle.get()
    outfit.choose_outfit(user_style)
    items = list()
    if (outfit.coat != None):
        items.append(outfit.coat)
    if (outfit.top2 != None):
        items.append(outfit.top2)
    items.append(outfit.top1)
    items.append(outfit.bottom)
    items.append(outfit.footwear)
    global curr_outfit
    curr_outfit = database.iloc[items]

    db_view["column"] = list(curr_outfit.columns)
    db_view["show"] = "headings"
    for column in db_view["columns"]:
        db_view.heading(column, text=column)

    rows = curr_outfit.to_numpy().tolist()
    for row in rows:
        db_view.insert("", "end", values=row)

    outfit.coat = None
    outfit.top2 = None

    return None

def change_items():
    global top
    top=Toplevel()
    top.geometry("400x450")
    items_label = LabelFrame(top, text='Select items to change:', padx=10, pady=10)
    items_label.grid(row=0, column=0, padx=15, pady=15)
    answers = list()
    for i in range(len(curr_outfit)):
        var = IntVar()
        c = Checkbutton(items_label, text = curr_outfit.iloc[i]['ID'], variable=var)
        c.deselect()
        c.pack(anchor=W)
        answers.append([var,c])

    submit_button = Button(top, text='Change selected items', command= lambda: update_items(answers))
    submit_button.grid(row=1, column=0, padx=10, pady=10)

    
    return None

def update_items(answers):

    new_outfit = outfit.change_items(curr_outfit, answers)

    change_label = LabelFrame(top, text='Outfit', padx=10, pady=10)
    change_label.place(x=15, y=250, height=190, width=380)

    outfit_view = ttk.Treeview(change_label)
    outfit_view.place(relheight=1, relwidth=1)

    scroll_y = Scrollbar(change_label, orient= VERTICAL, command= outfit_view.yview)
    scroll_x = Scrollbar(change_label, orient= HORIZONTAL, command= outfit_view.xview)    

    outfit_view.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side='bottom', fill='x')
    scroll_y.pack(side='right', fill='y')

    outfit_view["column"] = list(new_outfit.columns)
    outfit_view["show"] = "headings"
    for column in outfit_view["columns"]:
        outfit_view.heading(column, text=column)

    rows = new_outfit.to_numpy().tolist()
    for row in rows:
        outfit_view.insert("", "end", values=row)


global database
database = pd.read_csv('Clothes_database.csv')
root = Tk()
root.title('Clothes itemizer')
root.geometry('430x520')

title = Label(root, text='Smart Closet v0.4\nGood day, user! Please follow the instructions in the terminal to authenticate.', padx=10, pady=10)
title.grid(row=0, column=0, columnspan=6,sticky=N)

need_cold,need_wind,need_rain,temp, wind, weather = w_api.weather_api()
events = c_api.calendar_api(c_api.credentials)
keywords = get_keywords(events)

weather_label = Label(root, text='Weather forecast:\n'+weather)
temperature_label = Label(root, text="Temperature:\n"+str(temp)+' °C')
wind_label = Label(root, text='Wind speed:\n'+str(wind)+' m/s')

weather_label.grid(row=1,column=0, columnspan=2)
temperature_label.grid(row=1,column=2,columnspan=2)
wind_label.grid(row=1,column=4, columnspan=2)

style_label = LabelFrame(root, text= 'Style',pady=15, padx=15)
style_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
event_label = LabelFrame(root, text= 'Events',pady=15, padx=15)
event_label.grid(row=2, column=3, columnspan=3, padx=10, pady=10)

styles = ['Casual', 'Classy-casual', 'Classy']
global radioStyle
radioStyle = StringVar()
radioStyle.set('Casual')
for style in styles:
    button_s = Radiobutton(style_label, text = style, variable = radioStyle, value = style)
    button_s.pack(anchor=W)
global user_style
user_style = radioStyle.get()

if len(events)!=0:
    if len(events) > 3:
        for i in range(3):
            ev_label = Label(event_label, text=events[i])
            ev_label.pack(anchor=W)
    else:
        for i in range(len(events)):
            ev_label = Label(event_label, text=events[i])
            ev_label.pack(anchor=W)
else:
    ev_label = Label(event_label, text='No events today')
    ev_label.pack(anchor=W)

for elem in keywords:
    if(elem == 'party' and user_style != 'Classy'):
        user_style = 'Classy-casual'
    elif(elem == 'office' or elem == 'meeting'):
        user_style = 'Classy'

match(user_style):
    case 'Casual':
        remove_casual()
    case 'Classy-casual':
        do_nothing()
    case 'Classy':
        remove_classy()
    case _:
        do_nothing()

database_label = LabelFrame(root, text = 'Outfit', padx=10, pady=10)
database_label.place(height=190, width=400, x=15, y=240)

global db_view
db_view = ttk.Treeview(database_label)
db_view.place(relheight=1, relwidth=1)  

scroll_y = Scrollbar(database_label, orient= VERTICAL, command= db_view.yview)
scroll_x = Scrollbar(database_label, orient= HORIZONTAL, command= db_view.xview)

db_view.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
scroll_x.pack(side='bottom', fill='x')
scroll_y.pack(side='right', fill='y')

global outfit
outfit = oc.Outfit(need_cold,need_wind,need_rain,database)
outfit.choose_outfit(user_style)

outfit_button = Button(root, text='Suggest outfit', command = update_table)
outfit_button.place(x = 30, y = 440)
change_button = Button(root, text='Change items', command=change_items)
change_button.place(x = 30, y = 475)

update_table()



root.mainloop()