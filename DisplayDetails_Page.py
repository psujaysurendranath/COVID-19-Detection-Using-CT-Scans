# Author : Janvi D. Patil

#import tkinter as tk
from tkinter import *
#import sqlite3
import json
#import os
#import datetime
import requests
#from ScanDetails_Page import ScanDetails_Page
from tkinter import messagebox
window=Tk()
window.title("Details")
window.geometry('800x800')


def get_info(details):
    data_folder = 'Patient Data/'
    #details=lbl_text.get()

    with open(data_folder+details['patient_id']+'/'+details['patient_id']+'_data.json', 'r') as patient_file:
        data=json.load(patient_file)
        patient_id=data[patient_id]
        patient_name=data['name']
        patient_age=data['age']
        patient_country=data['country']
        final=(patient_name,patient_age,patient_country)
        return (final)
        patient_file.close()



    #name=data['name']
def display():
    details=lbl_text.get()
    information=get_info(details)
    if information:
        pass
    else:
        messagebox.showerror('Error','Cannot find patient_id {}'.format(details))


lbl=Label(window, text="Enter patient id:")
lbl.grid(column=0, row=0, sticky=E)
lbl_text=StringVar()

lbl_entry=Entry(window,textvariable=lbl_text, width=30)
lbl_entry.grid(column=1, row=0, sticky=W)
#details= lbl_txt.get()

btn=Button(window, text="Get information", command=display)
btn.grid(column=0, row=2,sticky=E)

name_label=Label(window, text='Full Name')
name_label.grid(column=0,row=3)

age_label=Label(window,text='Age')
age_label.grid(column=0,row=4)

country_label=Label(window,text='Country')
country_label.grid(column=0, row=5)


#output_txt=StringVar()
#lbl_output=Label(window, textvariable=output_txt)
#lbl_output.grid(column=0, row=4, sticky=W)
window.mainloop()