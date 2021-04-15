# Author : Nidhi S. Gosavi

import tkinter as tk
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