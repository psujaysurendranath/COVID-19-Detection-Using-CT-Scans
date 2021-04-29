# Author : Janvi D. Patil

from tkinter import messagebox, filedialog
import tkinter as tk
import os
from PIL import Image, ImageTk
import datetime
import sqlite3
import json
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import threading
import webbrowser
from appdirs import user_data_dir
#import requests
#from pydrive.files import GoogleDriveFile
#from pydrive.drive import GoogleDrive

from DisplayDetails_Page import DisplayDetails_Page

class ScanDetails_Page(tk.Frame):
    def __init__(self, parent = None, patient_id = '', model_list = None):
        tk.Frame.__init__(self, parent, width = 1000, height = 700)
        
        
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

        
        self.update_patient = patient_id

        if not bool(self.update_patient):
            self.last_patient_id, self.last_patient_name = self.get_latest_patient()

        else:
            self.last_patient_id = self.update_patient

            rtrn_btn = tk.Button(self, text = "Show Details", width = 20, command = lambda: self.NextPage())
            rtrn_btn.place(relx = 0.5 , y = 670, anchor = tk.CENTER)            


        with open(self.datapath + 'Patient Data/' + str(self.last_patient_id) + '/' + str(self.last_patient_id) + '_data.json', 'r') as patient_file:
            self.details = json.load(patient_file)
            
        self.last_patient_name = self.details['name']

        patient_file.close()

        
        self.classes = {'Covid Positive': 0, 'Healthy': 1, 'Other Infection': 2}

        self.img_no = len(os.listdir(self.datapath + 'Patient Data/' + self.last_patient_id)) - 1


        self.pred_disable = False


        if self.img_no > 1:
            self.img_nxt_btn = tk.Button(self, text = ">", command = lambda: self.chng_img('+'))
            
            self.img_prev_btn = tk.Button(self, text = "<", command = lambda: self.chng_img('-'))
        
        if self.last_patient_id + '_scan_' + str(self.img_no) +'.png' not in os.listdir(self.datapath + 'Patient Data/' + str(self.last_patient_id)):
            self.filepath = ''

        else:
            self.filepath = self.datapath + 'Patient Data/' + str(self.last_patient_id) + '/' + self.last_patient_id + '_scan_' + str(self.img_no) +'.png'
            self.pred_disable = True


        head = tk.Label(self, text = "COVID-19 PREDICTION USING CT-SCANS", font = "comicsansms 19 bold", bg = "black", fg = "white", padx = 5, pady = 5, relief = tk.SUNKEN, width = 1000)
        head.place(relx = 0.5, y = 20, anchor = tk.CENTER)


        patient_id_lbl = tk.Label(self, text = "Patient ID :", font = ("bold", 10))
        patient_id_lbl.place(relx = 0.02, y = 60, anchor = tk.W)

        patient_id = tk.Label(self, text = self.last_patient_id, font = ("bold", 10))
        patient_id.place(in_ = patient_id_lbl, relx = 1, rely = -0.1)

               
        patient_name = tk.Label(self, text = self.last_patient_name, font = ("bold", 10))
        patient_name.place(relx = 0.98, y = 60, anchor = tk.E)

        patient_name_lbl = tk.Label(self, text = "Patient Name :", font = ("bold", 10))
        patient_name_lbl.place(in_ = patient_name, relx = -0.1, rely = -0.1, anchor = tk.NE)


        Change_btn = tk.Button(self, text = "Change Details", width = 20,
                          command = lambda: self.change_details())
        Change_btn.place(relx = 0.5 , y = 550, anchor = tk.CENTER)


        Choose_btn = tk.Button(self, text = "Choose File", width = 20,
                          command = lambda: self.add_file())
        Choose_btn.place(relx = 0.5 , y = 590, anchor = tk.CENTER)

        
        self.Predict_btn = tk.Button(self, text = "Predict", width = 20, bg = "blue",fg = 'white',
                          command=lambda: self.predict_n_save_file())
        self.Predict_btn.place(relx = 0.5 , y = 630, anchor = tk.CENTER)

        if self.pred_disable:
            self.Predict_btn.config(state = 'disable')
            self.show_image()

        
        #Quit_btn = tk.Button(self, text = "Quit", width = 20,
        #                  command = lambda: [#self.destroy(),
        #                                     self.quit()])
        #Quit_btn.place(relx = 0.5 , y = 670, anchor = tk.CENTER)


        if bool(model_list):
            self.model_list = model_list
            #self.model.join()
            #print(self.model.predict())



    def database_conn(self):
        try:
            self.conn = sqlite3.connect(self.datapath + 'Patient Data/Patients_covid_data.db')
            
            with self.conn:
                self.cursor = self.conn.cursor()
                
            return True

        except:
            messagebox.showerror('Database Connection Error', 'Please check if "Patients_covid_data.db" exists in "Patient Data/" Folder')
            
            return False



    def get_latest_patient(self):        
        database = self.database_conn()
        
        if database:
            self.cursor.execute("SELECT Patient_ID, Full_Name FROM Patients_Data_Ovrview ORDER BY Patient_ID DESC LIMIT 1")
            #print(cursor.fetchall()[0])
            self.last_patient_id, self.last_patient_name = self.cursor.fetchall()[0]
            #print(self.last_patient_id)

            return self.last_patient_id, self.last_patient_name


    def change_details(self):
        from Registration_Page import Registration_Page

        self.destroy()

        prevWin = Registration_Page(patient_id = self.last_patient_id, model_list = self.model_list)
        prevWin.pack()
        prevWin.start()
        


    def add_file(self):
        #global filepath
        self.filepath = tk.StringVar()
        
        self.filepath = filedialog.askopenfilename(defaultextension = ".png", filetypes = [("All files", "*.*"), ("images", "*.png")])
        #print(filepath)
        
        #new_window = tkinter.Toplevel(root)
        
        #image = tkinter.PhotoImage(file = f)
        
        #l1 = tkinter.Label(new_window, image = image)
        #l1.image = image
        #l1.pack()
        self.show_image()


    
    def chng_img(self, chng):
        if chng == '+':
            img_no = int(self.filepath[-5])
            if img_no + 1 > len(os.listdir(self.datapath + 'Patient Data/' + self.last_patient_id)) - 1:
                pass

            else:
                img_no += 1

                self.filepath = self.filepath[0:-5] + str(img_no) + '.png'

                #print(self.filepath[0:-5] + str(img_no) + '.png')

                #print(self.filepath)

                self.show_image()


        elif chng == '-':
            img_no = int(self.filepath[-5])
            if img_no - 1 < 1:
                pass

            else:
                img_no -= 1

                self.filepath = self.filepath[0:-5] + str(img_no) + '.png'

                #print(self.filepath[-33:])
                #print(self.filepath[0:-5] + str(img_no) + '.png')

                #print(self.filepath)

                self.show_image()


    
    def show_image(self):
        if self.filepath:
            self.im = Image.open(self.filepath)
            self.im = self.im.resize((596, 447))
            #im.save('Patient Data/' + self.last_patient_id + '/' + self.last_patient_id+'_scan.png')
            tkimage = ImageTk.PhotoImage(self.im)
            
            imglabel = tk.Label(self, image = tkimage)
            imglabel.image = tkimage
            imglabel.place(relx = 0.5, rely = 0.43, anchor = tk.CENTER)

            #imglabel = tk.Label(self)
            #imglabel.place(relx = 0.5, rely = 0.43, anchor = tk.CENTER)


            if self.datapath + 'Patient Data/' not in self.filepath:
                self.pred_disable = False

                self.Predict_btn.config(state = 'normal')

                if self.img_no > 1:
                    self.img_nxt_btn.config(state = 'disabled')
                    self.img_prev_btn.config(state = 'disabled')

            else:
                self.pred_disable = True

                self.Predict_btn.config(state = 'disabled')


                if self.img_no > 1:
                    self.img_nxt_btn.place(in_ = imglabel, relx = 1.01, y = 222)
                    self.img_prev_btn.place(in_ = imglabel, x = -25, y = 222)


                    img_no = int(self.filepath[-5])
                    if img_no + 1 > len(os.listdir(self.datapath + 'Patient Data/' + self.last_patient_id)) - 1:
                        self.img_nxt_btn.config(state = 'disabled')

                    else:
                        self.img_nxt_btn.config(state = 'normal')


                    if img_no - 1 < 1:
                        self.img_prev_btn.config(state = 'disabled')

                    else:
                        self.img_prev_btn.config(state = 'normal')



    def predict_n_save_file(self):
        if 'Model' in os.listdir():
            
            if 'model_resnet.h5' in os.listdir('Model/'):
                if self.filepath:
                    self.save_filename = self.last_patient_id + '_scan_' + str(self.img_no + 1) +'.png'
                    save_file = self.datapath + 'Patient Data/' + self.last_patient_id + '/' + self.save_filename
                    self.im.save(save_file)
            
                    patient_im = self.im_preprocess()

                    
                    try:
                        model = self.model_list[0]

                    except:
                        self.model_list = list()
            
                        t2 = threading.Thread(target = lambda model, arg1 : model.append(load_model(arg1)), args = (self.model_list, 'Model/model_resnet.h5',))

                        t2.start()

                        t2.join()


                        model = self.model_list[0]


                    self.prediction = np.argmax(model.predict(patient_im), axis = -1)
                    #print(self.prediction)

                    self.prediction_class = list(self.classes.keys())[self.prediction[0]]
                    #print(self.prediction_class)

                    self.update_data()
                    self.NextPage()

            else:
                messagebox.showerror('Model Not Found', 'Please check if "model_resnet.h5" exists in "Model/" Folder. If you have not downloaded it then download and place it in "Model/" Folder.')
                
                self.model_download()
            

        else:
            os.mkdir('Model')
            
            messagebox.showinfo('Model Download', 'Please Download "model_resnet.h5" and place it in "Model/" Folder.')

            self.model_download()



    
    def model_download(self):
        url = 'https://drive.google.com/file/d/1Vs3bhtxgB_Wo0mUQ3VQD9jEbDSvPdqxk/view?usp=sharing'

        reply_browser = messagebox.askyesnocancel('Download Model', 'Do you want to open the link in browser?\nPress Yes to open in Browser.\nPress No to just copy the link in your clipboard\nPress cancel to close the pop-up')
        
        if reply_browser:
            webbrowser.open(url, new = 0, autoraise = True)
        
        elif not reply_browser:
            self.clipboard_clear()
            self.clipboard_append(url)
            self.update()

        
        """
        # Download model automatically(not working)

        from pydrive.auth import GoogleAuth
        gauth = GoogleAuth(settings_file='../settings.yaml')
        # Try to load saved client credentials
        gauth.LoadCredentialsFile("../credentials.json")
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile("../credentials.json")

        drive = GoogleDrive(gauth)
        file_id = '1Vs3bhtxgB_Wo0mUQ3VQD9jEbDSvPdqxk'
        download_dir = 'Model/'

        #logger.debug("Trying to download file_id " + str(file_id))
        file6 = drive.CreateFile({'id': file_id})
        file6.GetContentFile(download_dir+'mapmob.zip')
        zipfile.ZipFile(download_dir + 'test.zip').extractall(UNZIP_DIR)
        tracking_data_location = download_dir + 'test.json'
        return tracking_data_location
        file_obj = drive.CreateFile({'id': '1Vs3bhtxgB_Wo0mUQ3VQD9jEbDSvPdqxk'})
        file_obj.GetContentFile('model_resnet.h5')
        """



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
        
        database = None
        
        database = self.database_conn()
        
        '''
        try:
            if bool(self.conn) and bool(self.cursor):
                pass

            else:
                database = self.database_conn()

        except:
            database = self.database_conn()
        '''

        #print(self.details)

        self.details['covid_status'] = list(self.details['covid_status'])
        
        if database:
            if len(self.details['covid_status']) == 0:
                self.cursor.execute('UPDATE Patients_Data_Ovrview SET first_COVID_status = ? WHERE patient_id = ?', (str(self.prediction_class), self.last_patient_id))
                self.cursor.execute('UPDATE Patients_Data_Ovrview SET latest_COVID_status = ? WHERE patient_id = ?', (str(self.prediction_class), self.last_patient_id))

                self.details['covid_status'].append(self.prediction_class)

            else:
                if self.prediction_class.lower() == 'healthy':
                    if 'covid positive' in self.details['covid_status'][len(self.details['covid_status']) - 1].lower():
                        self.cursor.execute('UPDATE Patients_Data_Ovrview SET latest_COVID_status = ? WHERE patient_id = ?', ('Recovered', self.last_patient_id))
                        
                        self.details['covid_status'].append("Recovered")
                    
                    else:
                        self.cursor.execute('UPDATE Patients_Data_Ovrview SET latest_COVID_status = ? WHERE patient_id = ?', (str(self.prediction_class), self.last_patient_id))
                        
                        self.details['covid_status'].append(self.prediction_class)

                else:
                    self.cursor.execute('UPDATE Patients_Data_Ovrview SET latest_COVID_status = ? WHERE patient_id = ?', (str(self.prediction_class), self.last_patient_id))
                        
                    self.details['covid_status'].append(self.prediction_class)


            self.cursor.execute('UPDATE Patients_Data_Ovrview SET Modify_Time = ? WHERE patient_id = ?', (current_datetime, self.last_patient_id))
            self.conn.commit()
            self.conn.close()

        
        self.details['modify_time'] = current_datetime

        self.details['covid_status_time'] = list(self.details['covid_status_time'])
        self.details['covid_status_time'].append(current_datetime)

        self.details['img_filenames'] = list(self.details['img_filenames'])
        self.details['img_filenames'].append(self.save_filename)


        with open(self.datapath + 'Patient Data/' + str(self.last_patient_id) + '/' + str(self.last_patient_id) + '_data.json', 'w') as patient_file:
            json.dump(self.details, patient_file)

        patient_file.close()


        #print(self.details)



    def NextPage(self):
        self.destroy()

        if bool(self.update_patient):
            nextWin = DisplayDetails_Page(patient_id = self.update_patient, model_list = self.model_list)
        
        else:
            nextWin = DisplayDetails_Page(model_list = self.model_list)
            
        nextWin.pack()
        nextWin.start()



    def start(self):
        self.mainloop()



if __name__ == "__main__":
    ScanDetails_Page_obj = ScanDetails_Page()
    
    ScanDetails_Page_obj.pack()
    ScanDetails_Page_obj.start()