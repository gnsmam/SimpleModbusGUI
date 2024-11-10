from Solplanet_serial_modbus import Solplanet_Serial_Modbus
from tkinter import *
from time import sleep

from random import randint ## for testing purposes (see refresh_monitoring_data method)

class SimpleGui():
    
    def __init__(self):
        self.slave_address = 3
        self.main_window = Tk() #instance of windows class
        self.main_window.geometry("800x800")
        self.main_window.title("SimpleModbus")
        self.main_window.configure(background="white")
        
        self.close_button = Button(master=self.main_window, text= "Close", font = ("Arial", 10), command = self.close)
        self.close_button.place(relx = 1.0, rely = 0.0, anchor = "ne")
        
        self.main_frame = Frame(master= self.main_window, background="white", relief=GROOVE, width=3)
        self.generate_main_menu()
        self.main_frame.pack(expand=True)
        
        self.main_window.mainloop() #place window, listen for events    
    
    def generate_main_menu(self):
        button1 = Button(master=self.main_frame, text="Simple Monitoring", font = ("Arial", 20), command=self.Simple_monitoring_button) #!button
        button2 = Button(master=self.main_frame,  text="Other functions", font = ("Arial", 15), command=self.Other_functions_button) #!button2
        button1.grid(row=0, column=0)
        button2.grid(row=1, column=0)
        

    def Simple_monitoring_button(self):
        self.delete_all_onscreen_widgets()
        self.monitoring_menu_1()

    def Other_functions_button(self):
        self.delete_all_onscreen_widgets()
        self.generate_others_menu()
        
    def delete_all_onscreen_widgets(self):
        to_delete = self.main_frame.grid_slaves()
        for widget in to_delete:
            widget.destroy()    

    def monitoring_menu_1(self):
        
        #TODO other data like PV v/a and AC v/a will be labels that will be placed/displaced, should not eat that much memory (I hope)
        
        sn_number = "LM08K09S22503221"
        model = "ASW8KH-T1"
        state = "normal"
        active_power = "6053"
        e_today = "3.3"
        e_total = "333.3"
        error_code = "0"
        
        model_and_sn_label = Label(master= self.main_frame, text=("SN: " + sn_number + ", Model: " + model), font = ("Arial", 10), bg="white")
        device_state_label = Label(master= self.main_frame, text=("Device state: " + state), font = ("Arial", 10), bg="white")
        active_power_label = Label(master= self.main_frame, text=("Active power: " + active_power), font = ("Arial", 10), bg="white")
        e_today_label = Label(master= self.main_frame, text=("E-today: " + e_today), font = ("Arial", 10), bg="white")
        e_total_label = Label(master= self.main_frame, text=("E-total: " + e_total), font = ("Arial", 10), bg="white")
        error_code_label = Label(master= self.main_frame, text=("Error code: " + error_code), font = ("Arial", 10), bg="white")
        model_and_sn_label.grid(row=0, column=0,ipadx=20, ipady=5)
        device_state_label.grid(row=1, column=0,ipadx=20, ipady=5)
        active_power_label.grid(row=2, column=0,ipadx=20, ipady=5)
        e_today_label.grid(row=3, column=0,ipadx=20, ipady=5)
        e_total_label.grid(row=4, column=0,ipadx=20, ipady=5)
        error_code_label.grid(row=5, column=0,ipadx=20, ipady=5)
        
        self.monitoring_frame = Frame(master=self.main_frame) #frame object used only to cancel refreshing, I know it's stupid
        cancel_refresh_button = Button(master=self.main_frame, text= "Cancel_reading", font = ("Arial", 10), command = self.cancel_refresh)
        cancel_refresh_button.grid(row=6, column=0, pady=100)
        
        self.back_button = Button(master=self.main_window, text= "Back", font = ("Arial", 10), command = self.back)
        self.back_button.pack(x=0,y=0)
        
        self.update_monitoring_data_1()

    def update_monitoring_data_1(self):
        #TODO PROBABLY NEED TO CHANGE THE WAY DATA IS BEING REFRESHED, good enough for now: its 2AM
        self.main_frame.update_idletasks()
        print("UPDATING DATA")
        to_update = self.main_frame.winfo_children()
        to_update[0]["text"] = "SN: " + "LM08K09S22503221" + ", Model: " + "ASW8KH-T1"
        to_update[1]["text"] = "Device state: " + "normal"
        to_update[2]["text"] = "Active power: " + str(randint(500,700))
        to_update[3]["text"] = "E-today: " + str(randint(3,10))
        to_update[4]["text"] = "E-total: " + str(randint(33,700))
        to_update[5]["text"] = "Error code: " + str(randint(0,99))
        
        self.monitoring_frame.after(3000, self.update_monitoring_data_1)

    def generate_others_menu(self):
        self.main_frame.configure(padx=20, pady=20)
        button_grid = Frame(master=self.main_frame, bg="white")
        button_grid.grid(row=0, column=0)
        
        slave_address_entry = Entry(master=button_grid, textvariable="slave_address", font = ("Arial", 10))
        slave_address_entry.grid(row=0, column=0, columnspan=2, pady=5)
        
        device_info_button = Button(master=button_grid, text="Device Info", font = ("Arial", 10), command=self.read_device_info)
        device_info_button.grid(row=1, column=0, pady=5)
        
        version_info_button = Button(master=button_grid, text="Version Info", font = ("Arial", 10), command=self.read_version_info)
        version_info_button.grid(row=1, column=1, pady=5)
        
        settings_info_button = Button(master=button_grid, text="Settings Info", font = ("Arial", 10), command=self.read_settings_info)
        settings_info_button.grid(row=2, column=0, pady=5)
        
        read_errors_button = Button(master=button_grid, text="Warrning/Errors", font = ("Arial", 10), command=self.read_errors)
        read_errors_button.grid(row=2, column=1, pady=5)
        
        all_measurments_button = Button(master=button_grid, text="All measurments", font = ("Arial", 10), command=self.read_measurments)
        all_measurments_button.grid(row=3, column=0, pady=5)
        
        placeholder_button = Button(master=button_grid, text="Placeholder", font = ("Arial", 10))
        placeholder_button.grid(row=3, column=1, pady=5)
        
        read_custom_register = Button(master=button_grid, text="Read custom Input Register", font = ("Arial", 10), command=self.read_custom_register)
        read_custom_register.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.output_box = Text(master=self.main_frame, width=50, state="disabled")
        self.output_box.grid(row=0, column=1, pady=5)
        
        self.back_button = Button(master=self.main_window, text= "Back", font = ("Arial", 10), command = self.back)
        self.back_button.place(x=0,y=0)
    
    def cancel_refresh(self):
        self.monitoring_frame.destroy()
        
    def close(self):
        self.main_window.destroy()    
    
    def back(self):
        self.main_frame.destroy()
        self.back_button.destroy()
        self.main_frame = Frame(master= self.main_window, background="white")
        self.generate_main_menu()
        self.main_frame.pack(expand=True)
        
    def read_device_info(self):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", "version \n")
        self.output_box.configure(state="disabled")
        
    def read_version_info(self):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", "version \n")
        self.output_box.configure(state="disabled")
        
    def read_settings_info(self):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", "version \n")
        self.output_box.configure(state="disabled")      
        
    def read_errors(self):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", "version \n")
        self.output_box.configure(state="disabled")        

    def read_measurments(self):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", "version \n")
        self.output_box.configure(state="disabled")

    def read_custom_register(self):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", "version \n")
        self.output_box.configure(state="disabled")
        
SimpleGui()














