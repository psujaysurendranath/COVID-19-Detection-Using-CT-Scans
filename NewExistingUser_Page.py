# Author : Nidhi S. Gosavi

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sqlite3
import os
from tensorflow.keras.models import load_model
import threading

from Registration_Page import Registration_Page

class NewExistingUser(tk.Frame):
    def __init__(self, parent = None, model_list = None):
        tk.Frame.__init__(self, parent, width = 1000, height = 700)
        
        head = tk.Label(self, text = "COVID-19 PREDICTION USING CT-SCANS", font = "comicsansms 19 bold", bg = "black", fg = "white", padx = 5, pady = 5, relief = tk.SUNKEN, width = 1000)
        head.place(relx = 0.5, y = 20, anchor = tk.CENTER)


        page_title = tk.Label(text="WELCOME !", font = "comicsansms 19 bold", height = 2)
        page_title.place(relx = 0.5, y = 80, anchor = tk.CENTER)


        new_user_btn = tk.Button(text = "NEW USER", height = 2, width = 40, bg = "blue", fg = "white", 
                                    command = lambda: self.RegistrationPage())
        new_user_btn.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER)


        exist_user_btn = tk.Button(text = "EXISTING USER", height = 2, width = 40, bg = "blue", fg = "white",
                                    command = lambda: self.ExistingUser())
        exist_user_btn.place(relx = 0.5, rely = 0.6, anchor = tk.CENTER)


        if not(bool(model_list)):
            self.model_list = list()
            
            t1 = threading.Thread(target = lambda model, arg1 : model.append(load_model(arg1)), args = (self.model_list, 'Model/model_resnet.h5',))

            t1.start()

        else:
            self.model_list = model_list
            
        
        try:
            if 'Patients_covid_data.db' in os.listdir('Patient Data'):
                curr_stat = tk.Button(text = "Current Statistics", 
                                        command = lambda: self.display_graph())
                curr_stat.place(relx = 0.5, rely = 0.9, anchor = tk.CENTER)


                self.t2 = threading.Thread(target = self.covid_stat)

                self.t2.start()

        except FileNotFoundError:
            pass


    
    def covid_stat(self):
        database = self.database_conn()

        self.labels = ['Healthy', 'Covid Positive', 'Other Infection', 'Recovered']
        self.values = []

        if database:
            self.cursor.execute('SELECT COUNT(latest_COVID_status) FROM Patients_Data_Ovrview WHERE latest_COVID_status = "Healthy"')
            healthy_cnt = int(self.cursor.fetchall()[0][0])
            self.values.append(healthy_cnt)

            self.cursor.execute('SELECT COUNT(latest_COVID_status) FROM Patients_Data_Ovrview WHERE latest_COVID_status = "Covid Positive"')
            covid_cnt = int(self.cursor.fetchall()[0][0])
            self.values.append(covid_cnt)

            self.cursor.execute('SELECT COUNT(latest_COVID_status) FROM Patients_Data_Ovrview WHERE latest_COVID_status = "Other Infection"')
            other_cnt = int(self.cursor.fetchall()[0][0])
            self.values.append(other_cnt)

            self.cursor.execute('SELECT COUNT(latest_COVID_status) FROM Patients_Data_Ovrview WHERE latest_COVID_status = "Recovered"')
            recvd_cnt = int(self.cursor.fetchall()[0][0])
            self.values.append(recvd_cnt)


            self.conn.close()



    def display_graph(self):
        self.t2.join()
        

        root = tk.Tk()


        colors = ['#ccff99', '#ffcccc', '#ffffcc', '#ccffff']

        figure1 = Figure(figsize = (6, 4)) 
        subplot1 = figure1.add_subplot(111)

        subplot1.bar(x = self.labels, height = self.values, color = colors, edgecolor = 'black')

        self.bar1 = FigureCanvasTkAgg(figure1, root) 
        self.bar1.get_tk_widget().pack(side = tk.LEFT, fill = tk.BOTH, expand = 0)
        

        figure2 = Figure(figsize = (6, 4)) 
        subplot2 = figure2.add_subplot(111)

        pieSizes = self.values
        
        explode = [0.1, 0.1, 0.1, 0.1]  
        
        subplot2.pie(pieSizes, colors = colors, explode = explode, labels = self.labels, autopct = '%1.1f%%', shadow = True, startangle = 90) 
        
        subplot2.axis('equal')  
        
        self.pie2 = FigureCanvasTkAgg(figure2, root)
        self.pie2.get_tk_widget().pack()


        root.mainloop()


    

    def database_conn(self):
        try:
            self.conn = sqlite3.connect('Patient Data/Patients_covid_data.db')
            
            with self.conn:
                self.cursor = self.conn.cursor()
                
            return True

        except:
            messagebox.showerror('Database Connection Error', 'Please check if "Patients_covid_data.db" exists in "Patient Data/" Folder')
            
            return False
        


    def RegistrationPage(self):
        self.destroy()

        nextWin = Registration_Page(model_list = self.model_list)

        nextWin.pack()
        nextWin.start()

    

    def ExistingUser(self):
        from DisplayDetails_Page import DisplayDetails_Page
        self.destroy()
        
        nextWin = DisplayDetails_Page(existing_patient = True, model_list = self.model_list)
            
        nextWin.pack()
        nextWin.start()



    def start(self):    
        self.mainloop()




if __name__ == '__main__':
    NewPageObj = NewExistingUser()

    NewPageObj.pack()
    NewPageObj.start()