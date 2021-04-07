# Author : Janvi D. Patil

import tkinter as tk
import tkinter.filedialog
import os
from PIL import Image, ImageTk
#import PIL
import datetime
import sqlite3
import json
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model

from DisplayDetails_Page import DisplayDetails_Page

class ScanDetails_Page(tk.Frame):
    def __init__(self, parent = None):
        tk.Frame.__init__(self, parent, width = 1000, height = 700)
        

        self.last_patient_id, self.last_patient_name = self.database()
        self.classes = {'Covid Positive': 0, 'Healthy': 1, 'Other Infection': 2}

        if str(self.last_patient_id) + '_scan.png' not in os.listdir('Patient Data/' + str(self.last_patient_id)):
            self.filepath = ''

        else:
            self.filepath = 'Patient Data/' + str(self.last_patient_id) + '/' + str(self.last_patient_id) + '_scan.png'
            
            self.show_image()


        head = tk.Label(self, text = "COVID-19 PREDICTION USING CT-SCANS", font = "comicsansms 19 bold", bg = "black", fg = "white", padx = 5, pady = 5, relief = tk.SUNKEN, width = 1000)
        head.place(relx = 0.5, y = 20, anchor = tk.CENTER)


        patient_id_lbl = tk.Label(self, text = "Patient Name :", font = ("bold", 10))
        patient_id_lbl.place(relx = 0.02, y = 60, anchor = tk.W)

        patient_id = tk.Label(self, text = self.last_patient_id, font = ("bold", 10))
        patient_id.place(in_ = patient_id_lbl, relx = 1, rely = -0.1)

               
        patient_name = tk.Label(self, text = self.last_patient_name, font = ("bold", 10))
        patient_name.place(relx = 0.98, y = 60, anchor = tk.E)

        patient_name_lbl = tk.Label(self, text = "Patient Name :", font = ("bold", 10))
        patient_name_lbl.place(in_ = patient_name, relx = -0.1, rely = -0.1, anchor = tk.NE)


        Choose_btn = tk.Button(self, text = "Choose File", width = 20,
                          command = lambda: self.add_file())
        Choose_btn.place(relx = 0.5 , y = 550, anchor = tk.CENTER)

        
        Predict_btn = tk.Button(self, text = "Predict", width = 20, bg = "Red",fg = 'white',
                          command=lambda: self.predict_n_save_file())
        Predict_btn.place(relx = 0.5 , y = 590, anchor = tk.CENTER)

        
        Quit_btn = tk.Button(self, text = "Quit", width = 20,
                          command = lambda: [#self.destroy(),
                                             self.quit()])
        Quit_btn.place(relx = 0.5 , y = 630, anchor = tk.CENTER)



    def database(self):
        self.conn = sqlite3.connect('Patient Data/Patients_covid_data.db')
        
        with self.conn:
            self.cursor = self.conn.cursor()
        
        self.cursor.execute("SELECT Patient_ID, Full_Name FROM Patients_Data_Ovrview ORDER BY Patient_ID DESC LIMIT 1")
        #print(cursor.fetchall()[0])
        self.last_patient_id, self.last_patient_name = self.cursor.fetchall()[0]
        #print(self.last_patient_id)

        return self.last_patient_id, self.last_patient_name



    def add_file(self):
        #global filepath
        self.filepath = tk.StringVar()
        
        self.filepath = tk.filedialog.askopenfilename(defaultextension = ".png", filetypes = [("All files", "*.*"), ("images", "*.png")])
        #print(filepath)
        
        #new_window = tkinter.Toplevel(root)
        
        #image = tkinter.PhotoImage(file = f)
        
        #l1 = tkinter.Label(new_window, image = image)
        #l1.image = image
        #l1.pack()
        self.show_image()


    
    def show_image(self):
        if self.filepath:
            self.im = Image.open(self.filepath)
            self.im = self.im.resize((596, 447))
            #im.save('Patient Data/' + self.last_patient_id + '/' + self.last_patient_id+'_scan.png')
            tkimage = ImageTk.PhotoImage(self.im)
            
            mylabel = tk.Label(self, image = tkimage)
            mylabel.image = tkimage
            mylabel.place(relx = 0.5, rely = 0.43, anchor = tk.CENTER)



    def predict_n_save_file(self):
        if self.filepath:
            save_file = 'Patient Data/' + self.last_patient_id + '/' + self.last_patient_id+'_scan.png'
            self.im.save(save_file)
            
            patient_im = self.im_preprocess()

            model = load_model('Model/model_resnet.h5')
            
            self.prediction = np.argmax(model.predict(patient_im), axis = -1)
            #print(self.prediction)

            self.prediction_class = list(self.classes.keys())[self.prediction[0]]
            #print(self.prediction_class)

            self.update_data()
            self.NextPage()



    def im_preprocess(self):
        patient_im = Image.open(self.filepath)
        patient_im = patient_im.resize((192, 150))
        patient_im = np.array(patient_im)
        patient_im = cv2.cvtColor(patient_im, cv2.COLOR_BGR2GRAY)
        patient_im = patient_im / 255
        patient_im = np.expand_dims(patient_im, axis = 0)
        patient_im = np.expand_dims(patient_im, axis = 3)

        return patient_im



    def update_data(self):
        current_datetime_obj = datetime.datetime.now()
        #current_datetime_id = current_datetime_obj.strftime("%d%m%y%H%M%S")
        current_datetime = current_datetime_obj.strftime("%d/%b/%Y %H:%M:%S:%f")
        
        self.cursor.execute('UPDATE Patients_Data_Ovrview SET COVID_status = ? WHERE patient_id = ?', (str(self.prediction_class), self.last_patient_id))
        self.cursor.execute('UPDATE Patients_Data_Ovrview SET Modify_Time = ? WHERE patient_id = ?', (current_datetime, self.last_patient_id))
        self.conn.commit()
        self.conn.close()

        with open('Patient Data/' + str(self.last_patient_id) + '/' + str(self.last_patient_id) + '_data.json', 'r') as patient_file:
            details = json.load(patient_file)

        #print(details)

        details['covid_status'] = self.prediction_class
        details['modify_time'] = current_datetime

        patient_file.close()

        with open('Patient Data/' + str(self.last_patient_id) + '/' + str(self.last_patient_id) + '_data.json', 'w') as patient_file:
            json.dump(details, patient_file)

        patient_file.close()

        with open('Patient Data/' + str(self.last_patient_id) + '/' + str(self.last_patient_id) + '_data.json', 'r') as patient_file:
            details = json.load(patient_file)

        #print(details)



    def NextPage(self):
        nextWin = DisplayDetails_Page()
            
        nextWin.pack()
        nextWin.start()



    def start(self):
        self.mainloop()



if __name__ == "__main__":
    ScanDetails_Page_obj = ScanDetails_Page()
    
    ScanDetails_Page_obj.pack()
    ScanDetails_Page_obj.start()