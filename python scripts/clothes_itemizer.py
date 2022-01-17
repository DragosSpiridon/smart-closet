from tkinter import *
from tkinter import messagebox
import os
import pandas as pd
from csv import writer

global database
database = pd.read_csv(os.path.dirname(__file__) + '/../Clothes_database.csv')
root = Tk()
root.title('Clothes itemizer')
root.geometry('225x170')

def create_item():
    global top
    top=Toplevel()

    id_label = Label(top, text='ID: '+str(id), pady=10, padx=10)
    type_label = LabelFrame(top, text= 'Type',pady=10, padx=10)
    style_label = LabelFrame(top, text= 'Style',pady=23, padx=10)
    material_label = LabelFrame(top, text= 'Material', pady=10, padx=10)
    aesthetic_label = LabelFrame(top, text= 'Aesthetic', pady=10, padx=10)
    article_label = LabelFrame(top, text= 'Article', pady=10, padx=10)
    color_label = LabelFrame(top, text= 'Color', pady=10, padx=10)
    rain_label = LabelFrame(top, text= 'Rain',pady=10, padx=10)
    wind_label = LabelFrame(top, text= 'Wind',pady=10, padx=10)
    cold_label = LabelFrame(top, text= 'Cold',pady=10, padx=10)
    button_label = LabelFrame(top, pady=10, padx=10)

    id_label.grid(row=0, column=0, columnspan=4,sticky=N)
    type_label.grid(row=1, column=0)
    style_label.grid(row=1, column=1)
    material_label.grid(row=2, column=0,padx=5,pady=5)
    aesthetic_label.grid(row=2, column=1,padx=5,pady=5)
    article_label.grid(row=3, column=0,padx=5,pady=5)
    color_label.grid(row=3, column=1,padx=5,pady=5)
    rain_label.grid(row=4, column=0)
    wind_label.grid(row=4, column=1)
    cold_label.grid(row=5, column=0)
    button_label.grid(row=5, column=1)

    types = ['Outer', 'Top', 'Bottom', 'Footwear']
    styles = ['Casual', 'Classy-casual', 'Classy']
    global radioType, radioStyle, radioCold, radioWind, radioRain
    radioType = StringVar()
    radioType.set('Outer')
    radioStyle = StringVar()
    radioStyle.set('Casual')
    radioRain = IntVar()
    radioRain.set(0)
    radioWind = IntVar()
    radioWind.set(0)
    radioCold = IntVar()
    radioCold.set(0)

    for type in types:
        button_t = Radiobutton(type_label, text = type, variable = radioType, value = type)
        button_t.pack(anchor=W)
    for style in styles:
        button_s = Radiobutton(style_label, text = style, variable = radioStyle, value = style)
        button_s.pack(anchor=W)
    global material_entry, aesthetic_entry, article_entry, color_entry
    material_entry = Entry(material_label, width=20, borderwidth=5)
    aesthetic_entry = Entry(aesthetic_label, width=20, borderwidth=5)
    article_entry = Entry(article_label, width=20, borderwidth=5)
    color_entry = Entry(color_label, width=20, borderwidth=5)
    material_entry.pack()
    aesthetic_entry.pack()
    article_entry.pack()
    color_entry.pack()
    Radiobutton(rain_label, text= 'No', variable=radioRain, value = 0).pack(anchor=W)
    Radiobutton(rain_label, text= 'Yes', variable=radioRain, value = 1).pack(anchor=W)
    Radiobutton(wind_label, text= 'No', variable=radioWind, value = 0).pack(anchor=W)
    Radiobutton(wind_label, text= 'Yes', variable=radioWind, value = 1).pack(anchor=W)
    Radiobutton(cold_label, text= 'No', variable=radioCold, value = 0).pack(anchor=W)
    Radiobutton(cold_label, text= 'Yes', variable=radioCold, value = 1).pack(anchor=W)
    Button(button_label, text='Register', command = register_item).pack()
    Button(button_label, text='Cancel', command = top.destroy).pack()

def register_item():
    new_entry = [id,radioType.get(),article_entry.get(),radioStyle.get(),color_entry.get(),material_entry.get(),aesthetic_entry.get(),radioRain.get(),radioWind.get(),radioCold.get()]
    print(new_entry)
    print(type(new_entry))
    with open(os.path.dirname(__file__) + '/../Clothes_database.csv','a',newline='') as csv_file:
        writer_obj = writer(csv_file)
        writer_obj.writerow(new_entry)
        csv_file.close()

    top.destroy()

def check_database():
    global id
    id = int(entry.get())
    if id in database.values:
        messagebox.showwarning("Popup", "The item is already in the database.")
    else:
        response = messagebox.askyesno('Add item to database', 'ID is not found in database. Do you want to register it?')
    if response == 1:
        create_item()

label = Label(root, text='Enter code here:',padx=10, pady=10)
entry = Entry(root, width=35,borderwidth=5)
check_button = Button(root, text = 'Check database', command=check_database)
empty = Label(root, text=' ', padx=10, pady=10)

label.grid(row=0, column=0)
entry.grid(row=1, column=0)
empty.grid(row = 2, column = 0)
check_button.grid(row=3, column=0)



root.mainloop()
