# Author : Nidhi S. Gosavi

#from sqlite3.dbapi2 import Error
import tkinter as tk
from tkinter import messagebox
import sqlite3
import json
import os
import datetime
import re
from ScanDetails_Page import ScanDetails_Page

class Registration_Page(tk.Frame):
    def __init__(self, parent = None):
        tk.Frame.__init__(self, parent, width = 1000, height = 700)
        
                
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


        head = tk.Label(self, text = "COVID-19 PREDICTION USING CT-SCANS", font = "comicsansms 19 bold", bg = "black", fg = "white", padx = 5, pady = 5, relief = tk.SUNKEN)
        head.place(relx = 0.5, y = 20, anchor = tk.CENTER)


        page_title = tk.Label(self, text = "Registration form", width = 20, font = ("bold", 20))
        page_title.place(relx = 0.5, y = 70, anchor = tk.CENTER)


        name_vcmd = (self.register(self.name_callback))

        FirstName_entry = tk.Entry(self, textvar = self.FirstName_var)
        FirstName_entry.insert(tk.END, 'Enter First Name')
        FirstName_entry.place(relx = 0.5, y = 140, anchor = tk.CENTER)
        FirstName_entry.bind('<1>', self.EntryClick)
        FirstName_entry.configure(validate = 'all', validatecommand = (name_vcmd, '%P'))

        FirstName_lbl = tk.Label(self, text = "First Name", width = 20, font = ("bold", 10))
        FirstName_lbl.place(in_ = FirstName_entry, relx = -1.5, rely = 0)


        MiddleName_entry = tk.Entry(self, textvar = self.MiddleName_var)
        MiddleName_entry.insert(tk.END, 'Enter Middle Name')
        MiddleName_entry.place(relx = 0.5, y = 180, anchor = tk.CENTER)
        MiddleName_entry.bind('<1>', self.EntryClick)
        MiddleName_entry.configure(validate = 'all', validatecommand = (name_vcmd, '%P'))

        MiddleName_lbl = tk.Label(self, text = "Middle Name", width = 20, font = ("bold", 10))
        MiddleName_lbl.place(in_ = MiddleName_entry, relx = -1.5, rely = 0)


        LastName_entry = tk.Entry(self, textvar = self.LastName_var)
        LastName_entry.insert(tk.END, 'Enter Last Name')
        LastName_entry.place(relx = 0.5, y = 220, anchor = tk.CENTER)
        LastName_entry.bind('<1>', self.EntryClick)
        LastName_entry.configure(validate = 'all', validatecommand = (name_vcmd, '%P'))

        LastName_lbl = tk.Label(self, text = "Last Name", width = 20, font = ("bold", 10))
        LastName_lbl.place(in_ = LastName_entry, relx = -1.5, rely = 0)

        
        numeric_vcmd = (self.register(self.numeric_callback))    


        PhoneNo_entry = tk.Entry(self, textvar = self.PhoneNo_var)
        PhoneNo_entry.insert(tk.END, 'Enter Phone Number')
        PhoneNo_entry.place(relx = 0.5, y = 260, anchor = tk.CENTER)
        PhoneNo_entry.bind('<1>', self.EntryClick)
        PhoneNo_entry.configure(validate = 'all', validatecommand = (numeric_vcmd, '%P', 10))

        PhoneNo_lbl = tk.Label(self, text = "Phone Number", width = 20, font = ("bold", 10))
        PhoneNo_lbl.place(in_ = PhoneNo_entry, relx = -1.5, rely = 0)


        #email_vcmd = (self.register(self.email_callback))


        email_entry = tk.Entry(self, textvar = self.Email_var)
        email_entry.insert(tk.END, 'Enter email address')
        email_entry.place(relx = 0.5, y = 300, anchor = tk.CENTER)
        email_entry.bind('<1>', self.EntryClick)
        #email_entry.configure(validate = 'key', validatecommand = (email_vcmd, '%P'))

        email_lbl = tk.Label(self, text = "Email", width = 20, font = ("bold", 10))
        email_lbl.place(in_ = email_entry, relx = -1.5, rely = 0)


        Fem_RadBut = tk.Radiobutton(self, text = "Female", padx = 10, variable = self.Gender_var, value = 1)
        Mal_RadBut = tk.Radiobutton(self, text = "Male", padx = 4, variable = self.Gender_var, value = 2)
        Other_RadBut = tk.Radiobutton(self, text = "Others", padx = 4, variable = self.Gender_var, value = 3)

        Mal_RadBut.place(relx = 0.5, y = 340, anchor = tk.CENTER)
        Fem_RadBut.place(in_ = Mal_RadBut, relx = -1.5, rely = -0.25)
        Other_RadBut.place(in_ = Mal_RadBut, relx = 1, rely = -0.25)

        gender_lbl = tk.Label(self, text = "Gender", width = 10, font = ("bold", 10))
        gender_lbl.place(in_ = Fem_RadBut, relx = -1.37, rely = -0.1)


        country_list = ['Austria (AT)', 'Germany (DE)', 'India (IN)', 'South Korea (KR)', 'United Kingdom (GB)', 'United States (US)' ]
        

        country_drplst = tk.OptionMenu(self, self.Country_var, *country_list)
        country_drplst.config(width = 18)
        self.Country_var.set('Select Country')
        country_drplst.place(relx = 0.5, y = 380, anchor = tk.CENTER)
        country_drplst.extra = 'country_drplst'

        country_lbl = tk.Label(self, text="Country", width=20, font=("bold", 10))
        country_lbl.place(in_ = country_drplst, relx = -1.18, rely = 0)


        age_entry = tk.Entry(self, textvar = self.Age_var)
        age_entry.insert(tk.END, 'Enter Age')
        age_entry.place(relx = 0.5, y = 420, anchor = tk.CENTER)
        age_entry.bind('<1>', self.EntryClick)
        age_entry.configure(validate = 'all', validatecommand = (numeric_vcmd, '%P', 3))

        age_label = tk.Label(self, text = "Age", width = 20, font = ('bold', 10))
        age_label.place(in_ = age_entry, relx = -1.5, rely = 0)


        BldGrp_list = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']

        BldGrp_drplist = tk.OptionMenu(self, self.BloodGroup_var, *BldGrp_list)
        BldGrp_drplist.config(width = 18)
        self.BloodGroup_var.set('Select Blood Group')
        BldGrp_drplist.place(relx = 0.5, y = 470, anchor = tk.CENTER)
        BldGrp_drplist.extra = 'bldgrp_drplist'

        BldGrp_lbl = tk.Label(self, text = "Blood Group", width = 15, font = ('bold', 10))
        BldGrp_lbl.place(in_ = BldGrp_drplist, relx = -1.04, rely = 0)


        wght_entry = tk.Entry(self, textvar = self.Weight_var)
        wght_entry.insert(tk.END, 'Enter Weight')
        wght_entry.place(relx = 0.5, y = 510, anchor = tk.CENTER)
        wght_entry.bind('<1>', self.EntryClick)
        wght_entry.configure(validate = 'all', validatecommand = (numeric_vcmd, '%P', 3))

        wght_lbl = tk.Label(self, text = "Weight (in kgs.)", width = 20, font = ('bold', 10))
        wght_lbl.place(in_ = wght_entry, relx = -1.5, rely = 0)


        hght_entry = tk.Entry(self, textvar = self.Height_var)
        hght_entry.insert(tk.END, 'Enter Height')
        hght_entry.place(relx = 0.5, y = 550, anchor = tk.CENTER)
        hght_entry.bind('<1>', self.EntryClick)
        hght_entry.configure(validate = 'all', validatecommand = (numeric_vcmd, '%P', 3))

        hght_label = tk.Label(self, text = "Height (in cms.)", width = 20, font = ('bold', 10))
        hght_label.place(in_ = hght_entry, relx = -1.5, rely = 0)


        
        Submit_btn = tk.Button(self, text = 'Submit', width = 20, bg = "Red", fg = 'white',
                               command = lambda: self.EntryCheck())
        Submit_btn.place(relx = 0.5, y = 610, anchor = tk.CENTER)
        #Submit_btn.bind('<1>', Entrycheck)


    
    def EntryClick(self, event):
        if 'enter' in event.widget.get().lower():
            event.widget.delete(0, tk.END)
        
        '''elif event.widget.get():
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
        
        if name_re.match(self.MiddleName_var.get()) == None:
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
                self.store_details()
                self.destroy()
                self.NextPage()



    def store_details(self):
        details = {
            'create_time' : None,
            'modify_time' : None,
            'patient_id' : None,
            'name' : self.FirstName_var.get()+ " " + self.MiddleName_var.get()+ " " + self.LastName_var.get(),
            'phone_no' : int(self.PhoneNo_var.get()),
            'email' : self.Email_var.get(),
            'country' : self.Country_var.get(),
            'gender' : 'Male' if self.Gender_var.get() == 2 else 'Female' if self.Gender_var.get() == 1 else 'Others',
            'age' : int(self.Age_var.get()),
            'weight' : int(self.Weight_var.get()),
            'bloodgroup' : self.BloodGroup_var.get(),
            'height' : int(self.Height_var.get()),
            'covid_status' : 'NA'
        }


        if 'Patient Data' not in os.listdir():
            os.mkdir('Patient Data')


        details['create_time'], details['modify_time'], details['patient_id'] = self.database(details)

        
        data_folder = 'Patient Data/'


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



    def database(self, details):
        conn = sqlite3.connect('Patient Data/Patients_covid_data.db')
        
        with conn:
            cursor = conn.cursor()


        cursor.execute ('CREATE TABLE IF NOT EXISTS Patients_Data_Ovrview (Create_Time TEXT, Modify_Time TEXT, Patient_ID TEXT, Full_Name TEXT, Gender TEXT, Phone_No INT, Age INT, Country TEXT, COVID_status TEXT)')


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
        

        cursor.execute ('INSERT INTO Patients_Data_Ovrview (Create_Time, Modify_Time, Patient_ID, Full_Name, Gender, Phone_No, Age, Country, COVID_status) VALUES(?,?,?,?,?,?,?,?,?)',(current_datetime, current_datetime, current_patient_id, details['name'], details['gender'], details['phone_no'], details['age'], details['country'], 'NA'))


        conn.commit()


        return current_datetime, current_datetime, current_patient_id



    def NextPage(self):
        nextWin = ScanDetails_Page()
        
        nextWin.pack()
        nextWin.start()



    def start(self):
        self.mainloop()



if __name__ == "__main__":
    Registration_Page_obj = Registration_Page()
    
    Registration_Page_obj.pack()
    Registration_Page_obj.start()