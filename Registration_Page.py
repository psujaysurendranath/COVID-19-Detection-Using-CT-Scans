# Author : Nidhi S. Gosavi

#from sqlite3.dbapi2 import Error
import tkinter as tk
from tkinter import messagebox
import sqlite3
import json
import os
import datetime
import re
from tkinter.constants import ACTIVE
from tensorflow.keras.models import load_model
import threading
from appdirs import user_data_dir

#from ScanDetails_Page import ScanDetails_Page

class Registration_Page(tk.Frame):
    def __init__(self, parent = None, returning = False, patient_id = '', model_list = None):
        tk.Frame.__init__(self, parent, width = 1000, height = 700)
        
        self.middle_widg = ""

        self.FirstName_var = tk.StringVar()
        self.MiddleName_var = tk.StringVar()
        self.LastName_var = tk.StringVar()
        self.PhoneNo_var = tk.StringVar()
        self.Email_var = tk.StringVar()
        self.Gender_var = tk.IntVar()
        self.Country_var = tk.StringVar()
        self.Age_var = tk.StringVar()
        self.BloodGroup_var = tk.StringVar()
        self.Weight_var = tk.StringVar()
        self.Height_var = tk.StringVar()


        self.Error_Label = {}


        self.update_patient = patient_id


        head = tk.Label(self, text = "COVID-19 PREDICTION USING CT-SCANS", font = "comicsansms 19 bold", bg = "black", fg = "white", padx = 5, pady = 5, relief = tk.SUNKEN, width = 1000)
        head.place(relx = 0.5, y = 20, anchor = tk.CENTER)


        page_title = tk.Label(self, text = "Registration form", width = 20, font = ("bold", 20))
        page_title.place(relx = 0.5, y = 70, anchor = tk.CENTER)


        name_vcmd = (self.register(self.name_callback))

        self.FirstName_entry = tk.Entry(self, textvar = self.FirstName_var)
        self.FirstName_entry.insert(tk.END, 'Enter First Name')
        self.FirstName_entry.place(relx = 0.5, y = 140, anchor = tk.CENTER)
        self.FirstName_entry.bind('<1>', self.EntryClick)
        self.FirstName_entry.configure(validate = 'all', validatecommand = (name_vcmd, '%P'))

        FirstName_lbl = tk.Label(self, text = "First Name", width = 20, font = ("bold", 10))
        FirstName_lbl.place(in_ = self.FirstName_entry, relx = -1.5, rely = 0)


        self.MiddleName_entry = tk.Entry(self, textvar = self.MiddleName_var)
        self.MiddleName_entry.insert(tk.END, 'Enter Middle Name')
        self.MiddleName_entry.place(relx = 0.5, y = 180, anchor = tk.CENTER)
        self.MiddleName_entry.bind('<1>', self.EntryClick)
        self.MiddleName_entry.configure(validate = 'all', validatecommand = (name_vcmd, '%P'))

        MiddleName_lbl = tk.Label(self, text = "Middle Name", width = 20, font = ("bold", 10))
        MiddleName_lbl.place(in_ = self.MiddleName_entry, relx = -1.5, rely = 0)


        self.LastName_entry = tk.Entry(self, textvar = self.LastName_var)
        self.LastName_entry.insert(tk.END, 'Enter Last Name')
        self.LastName_entry.place(relx = 0.5, y = 220, anchor = tk.CENTER)
        self.LastName_entry.bind('<1>', self.EntryClick)
        self.LastName_entry.configure(validate = 'all', validatecommand = (name_vcmd, '%P'))

        LastName_lbl = tk.Label(self, text = "Last Name", width = 20, font = ("bold", 10))
        LastName_lbl.place(in_ = self.LastName_entry, relx = -1.5, rely = 0)

        
        numeric_vcmd = (self.register(self.numeric_callback))    


        self.PhoneNo_entry = tk.Entry(self, textvar = self.PhoneNo_var)
        self.PhoneNo_entry.insert(tk.END, 'Enter Phone Number')
        self.PhoneNo_entry.place(relx = 0.5, y = 260, anchor = tk.CENTER)
        self.PhoneNo_entry.bind('<1>', self.EntryClick)
        self.PhoneNo_entry.configure(validate = 'all', validatecommand = (numeric_vcmd, '%P', 10))

        PhoneNo_lbl = tk.Label(self, text = "Phone Number", width = 20, font = ("bold", 10))
        PhoneNo_lbl.place(in_ = self.PhoneNo_entry, relx = -1.5, rely = 0)


        #email_vcmd = (self.register(self.email_callback))


        self.email_entry = tk.Entry(self, textvar = self.Email_var)
        self.email_entry.insert(tk.END, 'Enter email address')
        self.email_entry.place(relx = 0.5, y = 300, anchor = tk.CENTER)
        self.email_entry.bind('<1>', self.EntryClick)
        #self.email_entry.configure(validate = 'key', validatecommand = (email_vcmd, '%P'))

        email_lbl = tk.Label(self, text = "Email", width = 20, font = ("bold", 10))
        email_lbl.place(in_ = self.email_entry, relx = -1.5, rely = 0)


        self.Fem_RadBut = tk.Radiobutton(self, text = "Female", padx = 10, variable = self.Gender_var, value = 1)
        self.Mal_RadBut = tk.Radiobutton(self, text = "Male", padx = 4, variable = self.Gender_var, value = 2)
        self.Other_RadBut = tk.Radiobutton(self, text = "Others", padx = 4, variable = self.Gender_var, value = 3)

        self.Mal_RadBut.place(relx = 0.5, y = 340, anchor = tk.CENTER)
        self.Fem_RadBut.place(in_ = self.Mal_RadBut, relx = -1.5, rely = -0.25)
        self.Other_RadBut.place(in_ = self.Mal_RadBut, relx = 1, rely = -0.25)

        gender_lbl = tk.Label(self, text = "Gender", width = 10, font = ("bold", 10))
        gender_lbl.place(in_ = self.Fem_RadBut, relx = -1.37, rely = -0.1)


        country_list = ['Austria (AT)', 'Germany (DE)', 'India (IN)', 'South Korea (KR)', 'United Kingdom (GB)', 'United States (US)' ]
        

        country_drplst = tk.OptionMenu(self, self.Country_var, *country_list)
        country_drplst.config(width = 18)
        self.Country_var.set('Select Country')
        country_drplst.place(relx = 0.5, y = 380, anchor = tk.CENTER)
        country_drplst.extra = 'country_drplst'

        country_lbl = tk.Label(self, text = "Country", width = 20, font = ("bold", 10))
        country_lbl.place(in_ = country_drplst, relx = -1.18, rely = 0)


        self.age_entry = tk.Entry(self, textvar = self.Age_var)
        self.age_entry.insert(tk.END, 'Enter Age')
        self.age_entry.place(relx = 0.5, y = 420, anchor = tk.CENTER)
        self.age_entry.bind('<1>', self.EntryClick)
        self.age_entry.configure(validate = 'all', validatecommand = (numeric_vcmd, '%P', 3))

        age_label = tk.Label(self, text = "Age", width = 20, font = ('bold', 10))
        age_label.place(in_ = self.age_entry, relx = -1.5, rely = 0)


        BldGrp_list = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']

        BldGrp_drplist = tk.OptionMenu(self, self.BloodGroup_var, *BldGrp_list)
        BldGrp_drplist.config(width = 18)
        self.BloodGroup_var.set('Select Blood Group')
        BldGrp_drplist.place(relx = 0.5, y = 470, anchor = tk.CENTER)
        BldGrp_drplist.extra = 'bldgrp_drplist'

        BldGrp_lbl = tk.Label(self, text = "Blood Group", width = 15, font = ('bold', 10))
        BldGrp_lbl.place(in_ = BldGrp_drplist, relx = -1.04, rely = 0)


        self.wght_entry = tk.Entry(self, textvar = self.Weight_var)
        self.wght_entry.insert(tk.END, 'Enter Weight')
        self.wght_entry.place(relx = 0.5, y = 510, anchor = tk.CENTER)
        self.wght_entry.bind('<1>', self.EntryClick)
        self.wght_entry.configure(validate = 'all', validatecommand = (numeric_vcmd, '%P', 3))

        wght_lbl = tk.Label(self, text = "Weight (in kgs.)", width = 20, font = ('bold', 10))
        wght_lbl.place(in_ = self.wght_entry, relx = -1.5, rely = 0)


        self.hght_entry = tk.Entry(self, textvar = self.Height_var)
        self.hght_entry.insert(tk.END, 'Enter Height')
        self.hght_entry.place(relx = 0.5, y = 550, anchor = tk.CENTER)
        self.hght_entry.bind('<1>', self.EntryClick)
        self.hght_entry.configure(validate = 'all', validatecommand = (numeric_vcmd, '%P', 3))

        hght_label = tk.Label(self, text = "Height (in cms.)", width = 20, font = ('bold', 10))
        hght_label.place(in_ = self.hght_entry, relx = -1.5, rely = 0)


        
        self.Submit_btn = tk.Button(self, text = 'Submit', width = 20, bg = "blue", fg = 'white',
                               command = lambda: self.EntryCheck())
        self.Submit_btn.place(relx = 0.5, y = 610, anchor = tk.CENTER)
        #self.Submit_btn.bind('<1>', Entrycheck)


        self.t1 = threading.Thread(target = self.importer)
        self.t1.start()


        # Works only for Windows
        #appdata_path = str(os.getenv('LOCALAPPDATA'))

        try:
            appdata_path = str(user_data_dir())

            if 'Covid Detection CT' not in os.listdir(appdata_path):
                os.mkdir(appdata_path + '/Covid Detection CT')

            self.datapath = appdata_path + '/Covid Detection CT/'


        except:
            self.datapath = ''


        if bool(self.update_patient):
            self.change_details()

        else:
            self.Prev_btn = tk.Button(self, text = 'Home Page', width = 20,
                                command = lambda: self.PreviousPage())
            self.Prev_btn.place(relx = 0.5, y = 650, anchor = tk.CENTER)


        self.model_list = model_list


    
    def importer(self):
        from ScanDetails_Page import ScanDetails_Page as ScanPage
        self.ScanDetails_Page = ScanPage


    
    def EntryClick(self, event):
        if 'enter' in event.widget.get().lower().split():
            event.widget.delete(0, tk.END)
        
        '''elif event.widget.get():x
            event.widget.select_range(0, tk.END)
            event.widget.icursor(tk.END)'''

        

    def numeric_callback(self, P, n):
        if str.isdigit(P) and len(str(P)) <= int(n) or P == "":
            return True
        
        else:
            return False


    
    def name_callback(self, P):
        return not str.isdigit(P)

    

    def name_email_check(self):
        email_re = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        name_re = re.compile(r"^[^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{1,}$")
        

        email_id = self.Email_var.get()
        #name = self.FirstName_var.get()+ " " + self.MiddleName_var.get()+ " " + self.LastName_var.get()

        
        if email_re.match(email_id) == None:
            messagebox.showerror("Error", "E-mail ID seems wrong")
            return False

        
        if name_re.match(self.FirstName_var.get()) == None or len(self.FirstName_var.get()) <= 2:
            messagebox.showerror("Error", "First Name seems wrong")
            return False
        

        if self.MiddleName_var.get() and "enter" not in self.MiddleName_var.get().lower():
            if self.MiddleName_var.get() != '' and name_re.match(self.MiddleName_var.get()) == None:
                messagebox.showerror("Error", "Middle Name seems wrong")
                return False

        if name_re.match(self.LastName_var.get()) == None:
            messagebox.showerror("Error", "Last Name seems wrong")
            return False


        return True



    def EntryCheck(self):
        rad_btn_count = 1
        
        for widg in self.winfo_children():
            if widg in self.Error_Label.keys():
                self.Error_Label[widg].destroy()
                self.Error_Label.pop(widg)

            if type(widg) not in (tk.Label, tk.Radiobutton, tk.OptionMenu, tk.Button):
                if "middle name" in widg.get().lower():
                    self.middle_widg = str(widg)
                    continue

                if str(widg) == self.middle_widg:
                    continue

                if not widg.get() or 'enter' in widg.get().lower():
                    self.Error_Label[widg] = tk.Label(self, text = "Compulory Field!", width = 20, font = ("bold", 10), fg = "red")
                    self.Error_Label[widg].place(in_ = widg, relx = 1.5)
                    widg.focus_set()


            elif type(widg) == tk.Radiobutton:
                if rad_btn_count < 3:
                    rad_btn_count += 1
                
                else:
                    if self.Gender_var.get() not in (1, 2, 3):
                        self.Error_Label[widg] = tk.Label(self, text = "Compulory Field!", width = 20, font = ("bold", 10), fg = "red")
                        self.Error_Label[widg].place(in_ = widg, relx = 1.5)
                        widg.focus_set()
                
                
            elif type(widg) == tk.OptionMenu:
                if widg.extra == 'country_drplst':
                    if not self.Country_var.get() or 'select' in self.Country_var.get().lower() and widg not in self.Error_Label.keys():
                        self.Error_Label[widg] = tk.Label(self, text = "Compulory Field!", width = 20, font = ("bold", 10), fg = "red")
                        self.Error_Label[widg].place(in_ = widg, relx = 1.34)
                        widg.focus_set()

                else:                        
                    if not self.BloodGroup_var.get() or 'select' in self.BloodGroup_var.get().lower() and widg not in self.Error_Label.keys():
                        self.Error_Label[widg] = tk.Label(self, text = "Compulory Field!", width = 20, font = ("bold", 10), fg = "red")
                        self.Error_Label[widg].place(in_ = widg, relx = 1.34)
                        widg.focus_set()

        if bool(self.Error_Label):
            messagebox.showerror("Error", "Please fill in all the details!")

        else:
            if self.name_email_check():
                if not bool(self.update_patient):
                    self.store_details()

                else:
                    self.update_details()

                self.destroy()
                self.NextPage()



    def change_details(self):
        with open(self.datapath + 'Patient Data/' + str(self.update_patient) + '/' + str(self.update_patient) + '_data.json', 'r') as patient_file:
            self.details = json.load(patient_file)


        name = self.details['name']
       
        self.FirstName_entry.delete(0, tk.END)
        self.FirstName_entry.insert(0, name.split()[0])
        
        if len(name.split()) < 3:
            self.LastName_entry.delete(0, tk.END)
            self.LastName_entry.insert(0, name.split()[1])

        else:
            self.MiddleName_entry.delete(0, tk.END)
            self.MiddleName_entry.insert(0, name.split()[1])

            self.LastName_entry.delete(0, tk.END)
            self.LastName_entry.insert(0, name.split()[2])

        self.PhoneNo_entry.delete(0, tk.END)
        self.PhoneNo_entry.insert(0, self.details['phone_no'])

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, self.details['email'])

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, self.details['email'])

        gender = self.details['gender']

        if gender.lower() == 'male':
            self.Mal_RadBut.select()

        elif gender.lower() == 'female':
            self.Fem_RadBut.select()

        else:
            self.Other_RadBut.select()
        
        self.Country_var.set(self.details['country'])

        self.age_entry.delete(0, tk.END)
        self.age_entry.insert(0, self.details['age'])

        self.BloodGroup_var.set(self.details['bloodgroup'])

        self.wght_entry.delete(0, tk.END)
        self.wght_entry.insert(0, self.details['weight'])

        self.hght_entry.delete(0, tk.END)
        self.hght_entry.insert(0, self.details['height'])

        self.Submit_btn.config(text = 'Update')
        

        patient_file.close()




    def store_details(self):
        mid_name = ""
        if self.MiddleName_var.get() and "enter" not in self.MiddleName_var.get().lower():
            mid_name = self.MiddleName_var.get()

        
        details = {
            'create_time' : None,
            'modify_time' : None,
            'patient_id' : None,
            'name' : self.FirstName_var.get()+ " " + mid_name + " " + self.LastName_var.get(),
            'phone_no' : int(self.PhoneNo_var.get()),
            'email' : self.Email_var.get(),
            'country' : self.Country_var.get(),
            'gender' : 'Male' if self.Gender_var.get() == 2 else 'Female' if self.Gender_var.get() == 1 else 'Others',
            'age' : int(self.Age_var.get()),
            'bloodgroup' : self.BloodGroup_var.get(),
            'weight' : int(self.Weight_var.get()),
            'height' : int(self.Height_var.get()),
            'covid_status' : [],
            'covid_status_time' : [],
            'img_filenames' : []
        }


        if 'Patient Data' not in os.listdir(self.datapath):
            os.mkdir(self.datapath + 'Patient Data')


        
        

        details['create_time'], details['modify_time'], details['patient_id'] = self.database(details)

        
        data_folder = self.datapath + 'Patient Data/'


        #if details['name'] not in os.listdir(data_folder):
        os.mkdir(data_folder+details['patient_id'])


        #print(details)


        with open(data_folder+details['patient_id']+'/'+details['patient_id']+'_data.json', 'w') as patient_file:
            json.dump(details, patient_file)

        patient_file.close()

        #nextWin = ScanDetails_Page()


        '''with open(data_folder+details['patient_id']+'/'+details['patient_id']+'_data.json', 'r') as patient_file_read:
            data = json.load(patient_file_read)
        
        print(data)

        patient_file_read.close()'''

    
    def update_details(self):
        mid_name = ""
        if self.MiddleName_var.get() and "enter" not in self.MiddleName_var.get().lower():
            mid_name = self.MiddleName_var.get()

        
        update_details = {
            'create_time' : self.details['create_time'],
            'modify_time' : self.details['modify_time'],
            'patient_id' : self.update_patient,
            'name' : self.FirstName_var.get()+ " " + mid_name + " " + self.LastName_var.get(),
            'phone_no' : int(self.PhoneNo_var.get()),
            'email' : self.Email_var.get(),
            'country' : self.Country_var.get(),
            'gender' : 'Male' if self.Gender_var.get() == 2 else 'Female' if self.Gender_var.get() == 1 else 'Others',
            'age' : int(self.Age_var.get()),
            'bloodgroup' : self.BloodGroup_var.get(),
            'weight' : int(self.Weight_var.get()),
            'height' : int(self.Height_var.get()),
            'covid_status' : self.details['covid_status'],
            'covid_status_time' : self.details['covid_status_time'],
            'img_filenames' : self.details['img_filenames'],
        }


        current_datetime = self.update_database(update_details)

        update_details['modify_time'] = current_datetime


        data_folder = self.datapath + 'Patient Data/'


        #print(details)


        with open(data_folder+update_details['patient_id']+'/'+update_details['patient_id']+'_data.json', 'w') as patient_file:
            json.dump(update_details, patient_file)

        patient_file.close()

        #nextWin = ScanDetails_Page()


        '''with open(data_folder+details['patient_id']+'/'+details['patient_id']+'_data.json', 'r') as patient_file_read:
            data = json.load(patient_file_read)
        
        print(data)

        patient_file_read.close()'''



    def database(self, details):
        conn = sqlite3.connect(self.datapath + 'Patient Data/Patients_covid_data.db')
        
        with conn:
            cursor = conn.cursor()


        cursor.execute ('CREATE TABLE IF NOT EXISTS Patients_Data_Ovrview (Create_Time TEXT, Modify_Time TEXT, Patient_ID TEXT, Full_Name TEXT, Gender TEXT, Phone_No INT, Age INT, Country TEXT, first_COVID_status TEXT, latest_COVID_status TEXT)')


        current_datetime_obj = datetime.datetime.now()
        current_datetime_id = current_datetime_obj.strftime("%d%m%y%H%M%S")
        current_datetime = current_datetime_obj.strftime("%d/%b/%Y %H:%M:%S:%f")


        cursor.execute("SELECT COUNT(*) FROM Patients_Data_Ovrview")
    
        if cursor.fetchall()[0][0] > 0:
            cursor.execute("SELECT Patient_ID FROM Patients_Data_Ovrview ORDER BY Patient_ID DESC LIMIT 1")
            #print(cursor.fetchall()[0][0])
            last_patient_id = cursor.fetchall()[0][0]
            #print(last_patient_id[3:8])
            last_patient_id = int(last_patient_id[3:8])
            num_of_zeros = ''
            num_of_zeros = '0' * (5 - len(str(last_patient_id + 1)))
            current_patient_id = 'CVD' + num_of_zeros + str(last_patient_id + 1) + current_datetime_id  + details['country'][-3 : -1]

        else:
            current_patient_id = 'CVD' + '00001' + current_datetime_id + details['country'][-3 : -1]
            #print(current_patient_id)
        

        cursor.execute ('INSERT INTO Patients_Data_Ovrview (Create_Time, Modify_Time, Patient_ID, Full_Name, Gender, Phone_No, Age, Country, first_COVID_status, latest_COVID_status) VALUES(?,?,?,?,?,?,?,?,?,?)',(current_datetime, current_datetime, current_patient_id, details['name'], details['gender'], details['phone_no'], details['age'], details['country'], 'NA', 'NA'))


        conn.commit()

        conn.close()


        return current_datetime, current_datetime, current_patient_id


    
    def update_database(self, details):
        conn = sqlite3.connect(self.datapath + 'Patient Data/Patients_covid_data.db')
        
        with conn:
            cursor = conn.cursor()


        current_datetime_obj = datetime.datetime.now()
        current_datetime = current_datetime_obj.strftime("%d/%b/%Y %H:%M:%S:%f")
        

        cursor.execute('UPDATE Patients_Data_Ovrview SET Modify_Time = ?, Full_Name = ?, Gender = ?, Phone_No = ?, Age = ?, Country = ? WHERE patient_id = ?',(current_datetime, details['name'], details['gender'], details['phone_no'], details['age'], details['country'], details['patient_id']))

        conn.commit()

        conn.close()


        return current_datetime



    def PreviousPage(self):
        from NewExistingUser_Page import NewExistingUser

        self.destroy()

        prevWin = NewExistingUser(model_list = self.model_list)

        prevWin.pack()
        prevWin.start()



    def NextPage(self):
        self.t1.join()
        if bool(self.update_patient):
            nextWin = self.ScanDetails_Page(patient_id = self.update_patient, model_list = self.model_list)

        else:
            nextWin = self.ScanDetails_Page(model_list = self.model_list)
        
        nextWin.pack()
        nextWin.start()



    def start(self):
        self.mainloop()



if __name__ == "__main__":
    Registration_Page_obj = Registration_Page()
    
    Registration_Page_obj.pack()
    Registration_Page_obj.start()