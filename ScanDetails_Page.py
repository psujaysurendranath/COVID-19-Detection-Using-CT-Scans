import tkinter as tk
import tkinter.filedialog
import os
from PIL import Image, ImageTk
#import PIL
import sqlite3

class ScanDetails_Page(tk.Frame):
    def __init__(self, parent = None):
        tk.Frame.__init__(self, parent, width = 1000, height = 700)
        
        last_patient_id, last_patient_name = self.database()
        
        def add_file():
            global filepath
            
            filepath = tk.StringVar()
            filepath = tk.filedialog.askopenfilename(defaultextension = ".png", filetypes = [("All files", "*.*"), ("images", "*.png")])
            #print(filepath)
            
            #new_window = tkinter.Toplevel(root)
            
            #image = tkinter.PhotoImage(file = f)
            
            #l1 = tkinter.Label(new_window, image = image)
            #l1.image = image
            #l1.pack()
            
            im = Image.open(filepath)
            im = im.resize((596, 447))
            im.save('Patient Data/' + last_patient_id + '/' + last_patient_id+'_scan.png')
            tkimage = ImageTk.PhotoImage(im)
            
            mylabel = tk.Label(self, image = tkimage)
            mylabel.image = tkimage
            mylabel.place(relx = 0.5, rely = 0.43, anchor = tk.CENTER)
        

        head = tk.Label(self, text = "COVID-19 PREDICTION USING X-RAYS", font = "comicsansms 19 bold", bg = "black", fg = "white", padx = 5, pady = 5, relief = tk.SUNKEN)
        head.place(relx = 0.5, y = 20, anchor = tk.CENTER)


        patient_id_lbl = tk.Label(self, text = "Patient Name :", font = ("bold", 10))
        patient_id_lbl.place(relx = 0.02, y = 60, anchor = tk.W)

        patient_id = tk.Label(self, text = last_patient_id, font = ("bold", 10))
        patient_id.place(in_ = patient_id_lbl, relx = 1, rely = -0.1)

               
        patient_name = tk.Label(self, text = last_patient_name, font = ("bold", 10))
        patient_name.place(relx = 0.98, y = 60, anchor = tk.E)

        patient_name_lbl = tk.Label(self, text = "Patient Name :", font = ("bold", 10))
        patient_name_lbl.place(in_ = patient_name, relx = -0.1, rely = -0.1, anchor = tk.NE)


        Choose_btn = tk.Button(self, text = "Choose File", width = 20,
                          command = lambda: add_file())
        Choose_btn.place(relx = 0.5 , y = 550, anchor = tk.CENTER)

        
        Predict_btn = tk.Button(self, text = "Predict", width = 20, bg = "Red",fg = 'white')
                          #command=lambda: add_file)
        Predict_btn.place(relx = 0.5 , y = 590, anchor = tk.CENTER)

        
        Quit_btn = tk.Button(self, text = "Quit", width = 20,
                          command = lambda: self.quit())
        Quit_btn.place(relx = 0.5 , y = 630, anchor = tk.CENTER)


    def database(self):
        conn = sqlite3.connect('Patient Data/Patients_covid_data.db')
        
        with conn:
            cursor = conn.cursor()
        
        cursor.execute("SELECT Patient_ID, Full_Name FROM Patients_Data_Ovrview ORDER BY Patient_ID DESC LIMIT 1")
        #print(cursor.fetchall()[0])
        last_patient_id, last_patient_name = cursor.fetchall()[0]
        #print(last_patient_id)

        return last_patient_id, last_patient_name


    def start(self):
        self.mainloop()

if __name__ == "__main__":
    ScanDetails_Page_obj = ScanDetails_Page()
    
    ScanDetails_Page_obj.pack()
    ScanDetails_Page_obj.start()