# Author : Janvi D. Patil

#import tkinter as tk
import tkinter as tk
import sqlite3
import json
import os
#import datetime
import requests
#from ScanDetails_Page import ScanDetails_Page
from tkinter import messagebox
from tkinter.ttk import *
from appdirs import user_data_dir



class DisplayDetails_Page(tk.Frame):
    def __init__(self, parent = None, existing_patient = False, patient_id = '', model_list = None):
        tk.Frame.__init__(self, parent, width = 1000, height = 700)
        
        head = tk.Label(self, text = "COVID-19 PREDICTION USING CT-SCANS", font = "comicsansms 19 bold", bg = "black", fg = "white", padx = 5, pady = 5, relief = tk.SUNKEN, width = 1000)
        head.place(relx = 0.5, y = 20, anchor = tk.CENTER)


        # Works only for Windows
        #appdata_path = str(os.getenv('LOCALAPPDATA'))

        try:
            appdata_path = str(user_data_dir())

            if 'Covid Detection CT' in os.listdir(appdata_path):
                self.datapath = appdata_path + '/Covid Detection CT/'

            elif 'Patient Data' in os.listdir():
                self.datapath = ''

        except:
            if 'Patient Data' in os.listdir():
                self.datapath = ''
        
        
        self.patient_id_text = tk.StringVar()
        self.patient_found = False
        self.details = {}
        self.existing_patient = existing_patient

        patient_id_vcmd = (self.register(self.patient_id_callback))

        if self.existing_patient:          
            patient_id_label = tk.Label(self, text = "Enter Patient ID", width = 30)
            patient_id_label.place(relx = 0.4, y = 80, anchor = tk.CENTER)
            
            self.patient_id_entry = tk.Entry(self, textvar = self.patient_id_text, width = 30)
            self.patient_id_entry.place(in_ = patient_id_label, relx = 1, rely = -0.1)
            self.patient_id_entry.configure(validate = 'all', validatecommand = (patient_id_vcmd, '%P', 22))
            #print(self.patient_id_text)


            get_info_btn = tk.Button(self, text = "Get Information", command = lambda: self.get_info())
            get_info_btn.place(relx = 0.5, y = 120, anchor = tk.CENTER)

        
        elif bool(patient_id):
            self.patient_id_text = patient_id
            self.get_info()


        else:
            self.last_patient_id, self.last_patient_name = self.database()
            self.patient_id_text = self.last_patient_id
            self.get_info()

        
        home_btn = tk.Button(self, text = "Home Page", command = lambda: self.go_home())
        home_btn.place(relx = 0.5, y = 670, anchor = tk.CENTER)

        if bool(model_list):
            self.model_list = model_list

        
                
        if 'Patient Data' in os.listdir(self.datapath):
            if len(os.listdir(self.datapath + 'Patient Data')) != 0:
                all_ptnt_btn = tk.Button(self, text = "Show All Patients", command = lambda: self.show_patients())
                all_ptnt_btn.place(relx = 0.8, y = 80, anchor = tk.CENTER)



    def patient_id_callback(self, P, n):
        if str.isalnum(P) and len(str(P)) <= int(n) or P == "":
            return True
        
        else:
            return False

    

    def database_conn(self):
        try:
            self.conn = sqlite3.connect(self.datapath + 'Patient Data/Patients_covid_data.db')
            
            with self.conn:
                self.cursor = self.conn.cursor()
                
            return True

        except:
            messagebox.showerror('Database Connection Error', 'Please check if "Patients_covid_data.db" exists in "Patient Data/" Folder')
            
            return False



    def database(self):
        database = self.database_conn()

        if database:
        
            self.cursor.execute("SELECT Patient_ID, Full_Name FROM Patients_Data_Ovrview ORDER BY Patient_ID DESC LIMIT 1")
            #print(cursor.fetchall()[0])
            self.last_patient_id, self.last_patient_name = self.cursor.fetchall()[0]
            #print(self.last_patient_id)

            return self.last_patient_id, self.last_patient_name



    def get_info(self):
        if self.existing_patient:
            if len(self.patient_id_text.get()) != 0:
                self.patient_id_text = self.patient_id_text.get()
            
            else:
                self.patient_id_text = tk.StringVar()
        
        data_folder = self.datapath + 'Patient Data/'
        #details=lbl_text.get()

        #print(self.patient_id_text)
        try:
            with open(data_folder + str(self.patient_id_text) + '/' + str(self.patient_id_text) + '_data.json', 'r') as patient_file:
                self.details = dict(json.load(patient_file))
            
            patient_file.close()
            self.display()

            

        except FileNotFoundError:
            messagebox.showerror('Error','Cannot find patient_id : ' + str(self.patient_id_text) + '.\nPlease Enter Valid and Existing Patient ID.')


        if self.existing_patient:
            if self.patient_id_text:
                self.patient_id_entry.delete(0, tk.END)
                self.patient_id_text = tk.StringVar()
                self.patient_id_entry.configure(textvar = self.patient_id_text)




    def display(self):
        create_time_label = tk.Label(self, text = "Record Created : ")
        create_time_label.place(relx = 0.02, y = 160, anchor = tk.W)

        create_time_ = tk.Label(self, text = str(self.details['create_time'][:-7]), font = ("bold", 10))
        create_time_.place(in_ = create_time_label, relx = 1, rely = -0.1)

        modify_time_ = tk.Label(self, text = str(self.details['modify_time'][:-7]), font = ("bold", 10))
        modify_time_.place(relx = 0.98, y = 160, anchor = tk.E)

        modify_time_label = tk.Label(self, text = "Record Modified : ")
        modify_time_label.place(in_ = modify_time_, relx = -0.01, rely = -0.1, anchor = tk.NE)
        
        
        patient_id_label = tk.Label(self, text = 'Patient ID', width = 30)
        patient_id_label.place(relx = 0.4, y = 190, anchor = tk.CENTER)
        
        patient_id_ = tk.Label(self, text = str(self.details['patient_id']), bg = 'white', width = 30, font = ('bold', 10))
        patient_id_.place(in_ = patient_id_label, relx = 1, rely = -0.1)
        

        name_label = tk.Label(self, text = 'Full Name', width = 30)
        name_label.place(relx = 0.4, y = 230, anchor = tk.CENTER)
        
        name_ = tk.Label(self, text = str(self.details['name']), bg = 'white', width = 30, font = ('bold', 10))
        name_.place(in_ = name_label, relx = 1, rely = -0.1)


        age_label = tk.Label(self, text = 'Age', width = 30)
        age_label.place(relx = 0.4, y = 270, anchor = tk.CENTER)

        age_ = tk.Label(self, text = str(self.details['age']) + ' years', bg = 'white', width = 30, font = ('bold', 10))
        age_.place(in_ = age_label, relx = 1, rely = -0.1)


        gender_label = tk.Label(self, text = 'Gender', width = 30)
        gender_label.place(relx = 0.4, y = 310, anchor = tk.CENTER)

        gender_ = tk.Label(self, text = str(self.details['gender']), bg = 'white', width = 30, font = ('bold', 10))
        gender_.place(in_ = gender_label, relx = 1, rely = -0.1)


        phone_label = tk.Label(self, text = 'Phone Number', width = 30)
        phone_label.place(relx = 0.4, y = 350, anchor = tk.CENTER)

        phone_ = tk.Label(self, text = str(self.details['phone_no']), bg = 'white', width = 30, font = ('bold', 10))
        phone_.place(in_ = phone_label, relx = 1, rely = -0.1)


        email_label = tk.Label(self, text = 'Email', width = 30)
        email_label.place(relx = 0.4, y = 390, anchor = tk.CENTER)

        email_ = tk.Label(self, text = str(self.details['email']), bg = 'white', width = 30, font = ('bold', 10))
        email_.place(in_ = email_label, relx = 1, rely = -0.1)


        bldgrp_label = tk.Label(self, text = 'Blood Group', width = 30)
        bldgrp_label.place(relx = 0.4, y = 430, anchor = tk.CENTER)

        bldgrp_ = tk.Label(self, text = str(self.details['bloodgroup']), bg = 'white', width = 30, font = ('bold', 10))
        bldgrp_.place(in_ = bldgrp_label, relx = 1, rely = -0.1)


        weight_label = tk.Label(self, text = 'Weight', width = 30)
        weight_label.place(relx = 0.4, y = 470, anchor = tk.CENTER)

        weight_ = tk.Label(self, text = str(self.details['weight']) + ' kg', bg = 'white', width = 30, font = ('bold', 10))
        weight_.place(in_ = weight_label, relx = 1, rely = -0.1)


        height_label = tk.Label(self, text = 'Height', width = 30)
        height_label.place(relx = 0.4, y = 510, anchor = tk.CENTER)

        height_ = tk.Label(self, text = str(self.details['height']) + ' cm', bg = 'white', width = 30, font = ('bold', 10))
        height_.place(in_ = height_label, relx = 1, rely = -0.1)


        country_label = tk.Label(self,text = 'Country', width = 30)
        country_label.place(relx = 0.4, y = 550, anchor = tk.CENTER)

        country_ = tk.Label(self, text = str(self.details['country']), bg = 'white', width = 30, font = ('bold', 10))
        country_.place(in_ = country_label, relx = 1, rely = -0.1)


        first_cvd_stat_label = tk.Label(self,text = 'First Covid Status', width = 30)
        first_cvd_stat_label.place(relx = 0.4, y = 590, anchor = tk.CENTER)

        first_cvd_stat_ = tk.Label(self, text = str(self.details['covid_status'][0]), bg = self.bgcolor(str(self.details['covid_status'][0])), width = 30, font = ('bold', 10))
        first_cvd_stat_.place(in_ = first_cvd_stat_label, relx = 1, rely = -0.1)


        full_progress_btn = tk.Button(self, text = "Full Progression", command = lambda : self.full_progress_info())
        full_progress_btn.place(in_ = first_cvd_stat_, relx = 1.14, rely = -0.1)


        if len(self.details['covid_status']) > 1:
            last = len(self.details['covid_status']) - 1

            latest_cvd_stat_label = tk.Label(self,text = 'Latest Covid Status', width = 30)
            latest_cvd_stat_label.place(relx = 0.4, y = 630, anchor = tk.CENTER)

            latest_cvd_stat_ = tk.Label(self, text = str(self.details['covid_status'][last]), bg = self.bgcolor(str(self.details['covid_status'][last])), width = 30, font = ('bold', 10))
            latest_cvd_stat_.place(in_ = latest_cvd_stat_label, relx = 1, rely = -0.1)


        update_scan_btn = tk.Button(self, text = "Update Scan/Details", command = lambda : self.update_scan_details())
        update_scan_btn.place(in_ = full_progress_btn, relx = -0.18, y = 30)



    def bgcolor(self, text):
        if 'covid' in text.lower():
            return '#ffcccc'

        elif 'healthy' in text.lower():
            return '#ccff99'

        elif 'other' in text.lower():
            return '#ffffcc'

        else:
            return '#ccffff'



    def update_scan_details(self):
        self.destroy()

        from ScanDetails_Page import ScanDetails_Page

        prev_win = ScanDetails_Page(patient_id = str(self.details['patient_id']), model_list = self.model_list)
        prev_win.pack()
        prev_win.start()


    
    def full_progress_info(self):
        self.id = 0
        self.iid = 0

        self.create_pop_up()

    

    def create_pop_up(self):
        root = tk.Tk()
        root.title('Full Patient Progression')
        #root.geometry('700x200')

        self.tree = Treeview(root, selectmode = "extended", columns = ('Status', 'Filename'))

        self.tree.heading('#0', text = 'Time')
        self.tree.heading('#1', text = 'Status')
        self.tree.heading('#2', text = 'Filename')
        self.tree.column('#0', stretch = tk.YES)
        self.tree.column('#1', stretch = tk.YES)
        self.tree.column('#2', minwidth = 0, width = 300, stretch = tk.YES)
        self.tree.pack(expand = tk.YES, fill = tk.BOTH)


        for i in range(len(self.details['covid_status_time'])):
            self.tree.insert('', 'end', iid = self.iid, text = self.details['covid_status_time'][i],
                                values = (self.details['covid_status'][i], 
                                            self.details['img_filenames'][i]))
            
            self.iid = self.iid + 1
            self.id = self.id + 1


        root.mainloop()



    def show_patients(self):
        root = tk.Tk()
        root.title('All Patients')
        #root.geometry('700x200')

        self.tree2 = Treeview(root, selectmode = "extended", columns = ('Status', 'Filename'))

        self.tree2.heading('#0', text = 'Patient ID')
        self.tree2.heading('#1', text = 'Patient Name')
        self.tree2.heading('#2', text = 'Covid Status')
        self.tree2.column('#0', stretch = tk.YES)
        self.tree2.column('#1', stretch = tk.YES)
        self.tree2.column('#2', stretch = tk.YES)
        self.tree2.pack(expand = tk.YES, fill = tk.BOTH)

        database = self.database_conn()

        if database:
            self.id = 0
            self.iid = 0

            for ptnt_id in list(os.listdir(self.datapath + 'Patient Data')):
                if ptnt_id.lower() == 'patients_covid_data.db':
                    continue

                self.cursor.execute("SELECT Full_Name, latest_COVID_status FROM Patients_Data_Ovrview WHERE Patient_ID = ?", (str(ptnt_id),))
                name, status = self.cursor.fetchall()[0]

                self.tree2.insert('', 'end', iid = self.iid, text = ptnt_id,
                                    values = (name, status))
                
                self.iid = self.iid + 1
                self.id = self.id + 1

        self.tree2.bind('<ButtonRelease-1>', self.ptnts_selectItem)
                

        root.mainloop()


    def ptnts_selectItem(self, a):
        curItem = self.tree2.focus()
        #print(self.tree2.item(curItem))

        patient_id = self.tree2.item(curItem)['text']
        
        try:
            self.clipboard_clear()
            self.clipboard_append(patient_id)
            self.update()

            messagebox.showinfo('Copied', 'Patient ID copied to clipboard')
        
        except:
            pass



    def go_home(self):
        self.destroy()

        from NewExistingUser_Page import NewExistingUser

        nextWin = NewExistingUser(model_list = self.model_list)
        nextWin.pack()
        nextWin.start()



    def start(self):    
        self.mainloop()



if __name__ == '__main__':
    DisplayDetails_obj = DisplayDetails_Page()

    DisplayDetails_obj.pack()
    DisplayDetails_obj.start()