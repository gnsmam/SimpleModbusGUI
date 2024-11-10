from Solplanet_serial_modbus import Solplanet_Serial_Modbus
from tkinter import *
from time import sleep

from random import randint ## for testing purposes (see refresh_monitoring_data method)

class SimpleGui(): 
    
    def __init__(self):
        
        self.client = Solplanet_Serial_Modbus(s_port = '/dev/ttyUSB0')
        
        self.slave_address = 3
        self.main_window = Tk() #instance of windows class
        self.main_window.minsize(800,600)
        self.main_window.title("SimpleModbus")
        self.main_window.configure(background="white")
        self.close_button = Button(master=self.main_window, text= "Close", font = ("Arial", 10), command = self.close)
        self.close_button.place(relx = 1.0, rely = 0.0, anchor = "ne")
        self.main_frame = Frame(master= self.main_window, background="white", relief=GROOVE, width=3)
        
        self.generate_main_menu()
        self.main_frame.pack(expand=True)
        
        
        self.global_width = self.main_window.winfo_width
        self.global_height = self.main_window.winfo_height
        
        self.main_window.mainloop() #place window, listen for events    
    
    def generate_main_menu(self):
        button1 = Button(master=self.main_frame, text="Simple Monitoring", font = ("Arial", 20), command=self.Simple_monitoring_button) #!button
        button2 = Button(master=self.main_frame,  text="Other functions", font = ("Arial", 15), command=self.Other_functions_button) #!button2
        button1.grid(row=0, column=0, pady=5)
        button2.grid(row=1, column=0, pady=5)
        
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
        self.back_button.place(x=0,y=0)
        
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
        
        
        
        modbus_address_frame = Frame(master=button_grid, bg="white")
        modbus_address_frame.grid(row=0, column=0, columnspan=2, pady=5, padx=2.5)
        
        self.modbus_label = Label(master= modbus_address_frame, text=("Input slave device address: (current: " +  str(self.slave_address) +")"), bg="white")
        self.modbus_label.grid(row=0, column=0, pady=5, padx=2.5)
        
        slave_address_entry = Entry(master=modbus_address_frame, font = ("Arial", 10))
        slave_address_entry.grid(row=0, column=1, columnspan=2, pady=5, padx=2.5)
        
        change_address_button = Button(master=modbus_address_frame, text="Change address", font = ("Arial", 10), command= lambda: self.change_modbus_address(slave_address_entry))
        change_address_button.grid(row=1, columnspan=3, pady=5, padx=2.5) 
        
        
        
        
        device_info_button = Button(master=button_grid, text="Device Info", font = ("Arial", 10), command=self.read_device_info, width=15)
        device_info_button.grid(row=1, column=0, pady=5, padx=2.5,sticky=E)
        
        version_info_button = Button(master=button_grid, text="Version Info", font = ("Arial", 10), command=self.read_version_info, width=15)
        version_info_button.grid(row=1, column=1, pady=5, padx=2.5,sticky=W)
        
        settings_info_button = Button(master=button_grid, text="Settings Info", font = ("Arial", 10), command=self.read_settings_info, width=15)
        settings_info_button.grid(row=2, column=0, pady=5, padx=2.5,sticky=E)
        
        read_errors_button = Button(master=button_grid, text="Warrning/Errors", font = ("Arial", 10), command=self.read_errors, width=15)
        read_errors_button.grid(row=2, column=1, pady=5, padx=2.5,sticky=W)
        
        all_measurments_button = Button(master=button_grid, text="All measurments", font = ("Arial", 10), command=self.read_measurments, width=15)
        all_measurments_button.grid(row=3, column=0, pady=5, padx=2.5,sticky=E) 
        
        placeholder_button = Button(master=button_grid, text="Placeholder", font = ("Arial", 10), width=15)
        placeholder_button.grid(row=3, column=1, pady=5, padx=2.5, sticky=W)
        
        
        
        custom_register_frame = Frame(master= button_grid, bg="white", borderwidth=2, relief=GROOVE)
        custom_register_frame.grid(row=4, column=0, columnspan=2)
        
        custom_register_label = Label(master= custom_register_frame, text=("Register to read:"), bg="white")
        custom_register_label.grid(row=1, column=0, pady=5, padx=2.5)
        custom_register_entry = Entry(master=custom_register_frame, font = ("Arial", 10))
        custom_register_entry.grid(row=2, column=0, pady=5, padx=2.5)
        
        custom_count_label = Label(master= custom_register_frame, text=("Register count:"), bg="white")
        custom_count_label.grid(row=1, column=1, pady=5, padx=2.5)
        custom_count_entry = Entry(master=custom_register_frame, font = ("Arial", 10))
        custom_count_entry.grid(row=2, column=1, pady=5, padx=2.5)
        
        read_custom_register = Button(master=custom_register_frame, text="Read custom Input Register", font = ("Arial", 10), 
                                command=lambda : self.read_custom_register(custom_register_entry, custom_count_entry), width=30)
        read_custom_register.grid(row=0, column=0, columnspan=2, pady=5, padx=2.5)
        
        
        self.output_box = Text(master=self.main_frame, width=50, state="disabled")
        self.output_box.grid(row=0, column=1, pady=0)
        clear_button = Button(master=self.main_frame, text="Clear output console", font = ("Arial", 10), command=self.clear_output_console, width=30)
        clear_button.grid(row=1, column=1, pady=5, padx=2.5)
        
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
        self.output_box.insert("end", "###########\n")
        try:
            #serial number:
            self.output_box.insert("end", "Serial number: "+ self.client.read_serial_number(self.slave_address) + "\n")
            #model
            self.output_box.insert("end", "Model: "+ self.client.read_machine_type(self.slave_address) + "\n")
            #device type
            self.output_box.insert("end", "Device type: "+ self.client.read_device_type(self.slave_address) + "\n")
            #rated power
            self.output_box.insert("end", "Rated power: "+ str(self.client.read_rated_power(self.slave_address)) + "W\n")
            #grid rated voltage and freq
            self.output_box.insert("end", "Grid rated voltage/frequency: "+ str(self.client.read_grid_rated_voltage(self.slave_address)) + "V/" + str(self.client.read_grid_rated_frequency(self.slave_address)) +"Hz\n")
            #e-total
            self.output_box.insert("end", "Serial number: "+ str(self.client.read_e_total(self.slave_address)) + "\n")
            #h-total
            self.output_box.insert("end", "H-total: "+ str(self.client.read_h_total(self.slave_address)) + "H\n")
            
        except:
            self.output_box.insert("end", "Connection failure\n")
        self.output_box.configure(state="disabled")  
    def read_version_info(self):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", "###########\n")
        try:
            #master:
            self.output_box.insert("end", "Master Version: "+ self.client.read_current_software_version(self.slave_address) + "\n")
            #slave:
            self.output_box.insert("end", "Slave Version: "+ self.client.read_current_slave_version(self.slave_address) + "\n")
            #safety:
            self.output_box.insert("end", "Safety Version: "+ self.client.read_current_safety_version(self.slave_address) + "\n")
        except:
            self.output_box.insert("end", "Connection failure\n")
        self.output_box.configure(state="disabled")  
        
    def read_settings_info(self):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", "###########\n")
        try:
            #current grid code
            self.output_box.insert("end", "Current grid code: "+ self.client.read_current_grid_code(self.slave_address) + "\n")
        except:
            self.output_box.insert("end", "Connection failure\n")
        self.output_box.configure(state="disabled")      
        
    def read_errors(self):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", "###########\n")
        try:
            #device state
            self.output_box.insert("end", "Deivce state: "+ self.client.read_device_state(self.slave_address) + "\n")
            #error code
            self.output_box.insert("end", "Error code: "+ str(self.client.read_error_message(self.slave_address)) + "\n")
            #warning code
            self.output_box.insert("end", "Current grid code: "+ str(self.client.read_warning_message(self.slave_address)) + "\n")
        except:
            self.output_box.insert("end", "Connection failure\n")
        self.output_box.configure(state="disabled")       

    def read_measurments(self):
        
        #PV voltage
        #PV current
        #AC voltage
        #AC current
        #internal temp
        #phase temp
        #bus voltage
        #string current
        #grid freq
        #apparent power
        #actrve power
        #reactive power
        #power factor
        
        self.output_box.configure(state="normal")
        self.output_box.insert("end", "version \n")
        self.output_box.configure(state="disabled")

    def read_custom_register(self, add_to_read, count_to_read):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", "###########\n")
        try:
            response = self.client.send_request_ir(address = int(add_to_read.get()), slave=self.slave_address, count = int(count_to_read.get()))
            self.output_box.insert("end", "Customer read result (not formatted):\n")
            for reg in response:
                self.output_box.insert("end", str(reg) + "\n")
            
        except:
            self.output_box.insert("end", "Error, please check the settings/connection" + "\n")
        self.output_box.configure(state="disabled")  
        
    def change_modbus_address(self, address):
        new_address = StringVar()
        new_address = address.get()  
        try: 
            self.slave_address = int(new_address)
            self.modbus_label["text"] = "Input slave device address: (current: " +  str(self.slave_address) +")"
            
            self.output_box.configure(state="normal")
            self.output_box.insert("end", "###########\n")
            self.output_box.insert("end", "Address changed to: " + str(self.slave_address) + "\n")
            self.output_box.configure(state="disabled")
            
        except ValueError:
            self.output_box.configure(state="normal")
            self.output_box.insert("end", "###########\n")
            self.output_box.insert("end", "INCORRECT ADDRESS FORMAT PROVIDED, PLEASE INPUT AN INTIGER \n")
            self.output_box.configure(state="disabled")
            
    def clear_output_console(self):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.configure(state="disabled")
        
SimpleGui()