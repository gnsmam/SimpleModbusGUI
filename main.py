#! /usr/bin/env
from Solplanet_serial_modbus import Solplanet_Serial_Modbus
from tkinter import *
from time import sleep

from random import randint ## for testing purposes (see refresh_monitoring_data method)

class SimpleGui(): 

    def __init__(self):

        self.port = ""
        self.slave_address = 0
        self.backup_address = 0

        self.main_window = Tk() #instance of windows class
        self.main_window.minsize(800,600)
        self.main_window.title("SimpleModbus")
        self.main_window.configure(background="#f0f0f0")
        self.main_frame = Frame(master= self.main_window, bg="#f0f0f0", relief=GROOVE, width=3)
        self.main_frame.pack(expand=True)
        
        self.input_window_startup()

        self.client = Solplanet_Serial_Modbus(s_port = self.port)
               
        self.main_window.mainloop() #place window, listen for events    
    
    def input_window_startup(self):
        port_label = Label(master= self.main_frame, text = "Input RS communication port: ", font = ("Arial", 15), bg="#f0f0f0")
        port_label_2 = Label(master= self.main_frame, text = "For Windows: you will find the port name in 'Device Manager', example: 'COM4'.\nExample for Linux: '/dev/ttyUSB0'.\nWarning: If provided port is incorrect, no functionality will be available.", font = ("Arial", 8), bg="#f0f0f0")
        port_entry = Entry(master=self.main_frame, font = ("Arial", 20), relief=GROOVE, borderwidth=3)

        modbus_label = Label(master= self.main_frame, text = "Input Device Modbus Address (for monitoring functionality): ", font = ("Arial", 15), bg="#f0f0f0")
        modbus_label_2 = Label(master= self.main_frame, text = "Note: If the device address was not changed, it is recommended to enter: '3'.", font = ("Arial", 8), bg="#f0f0f0")
        modbus_entry = Entry(master=self.main_frame, font = ("Arial", 20), relief=GROOVE, borderwidth=3)

        save_button = Button(master=self.main_frame, text="Save", font = ("Arial", 20), command= lambda: self.set_startup_parameters(port = port_entry, address = modbus_entry))

        port_label.grid(row=0, column=0)
        port_label_2.grid(row=1, column=0)
        port_entry.grid(row=2, column=0)

        modbus_label.grid(row=3, column=0)
        modbus_label_2.grid(row=4, column=0)
        modbus_entry.grid(row=5, column=0)

        save_button.grid(row=6, column=0, pady=10)

    def set_startup_parameters(self, port, address):
        self.slave_address = int(address.get())
        self.backup_address = self.slave_address
        self.port = port.get()
        self.generate_main_menu()

    def generate_main_menu(self):
        self.slave_address = self.backup_address
        print(self.port)
        print(self.slave_address)

        self.delete_all_onscreen_widgets()
        button1 = Button(master=self.main_frame, text="Simple Monitoring", font = ("Arial", 20), command=self.Simple_monitoring_button) #!button
        button2 = Button(master=self.main_frame,  text="Other functions", font = ("Arial", 20), command=self.Other_functions_button) #!button2
        button1.grid(row=0, column=0, pady=5)
        button2.grid(row=1, column=0, pady=5)
        close_button = Button(master=self.main_frame, text= "Exit", font = ("Arial", 15), command = self.close)
        close_button.grid(row=3, column=0, pady=5)     

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
        
        self.data_frame = Frame(master = self.main_frame, background="white", relief=GROOVE, borderwidth=3)
        self.data_frame.grid(row=0,column=0, ipady=5)

        model_and_sn_label = Label(master= self.data_frame, font = ("Arial", 10), bg="white")
        device_state_label = Label(master= self.data_frame, font = ("Arial", 10), bg="white")
        active_power_label = Label(master= self.data_frame, font = ("Arial", 10), bg="white")
        e_today_label = Label(master= self.data_frame, font = ("Arial", 10), bg="white")
        e_total_label = Label(master= self.data_frame, font = ("Arial", 10), bg="white")
        error_code_label = Label(master= self.data_frame, font = ("Arial", 10), bg="white")
        model_and_sn_label.grid(row=0, column=0,ipadx=20,ipady=5 )
        device_state_label.grid(row=1, column=0,ipadx=20,ipady=5)
        active_power_label.grid(row=2, column=0,ipadx=20, ipady=5)
        e_today_label.grid(row=3, column=0,ipadx=20, ipady=5)
        e_total_label.grid(row=4, column=0,ipadx=20, ipady=5)
        error_code_label.grid(row=5, column=0,ipadx=20)
        
        self.monitoring_frame = Frame(master=self.main_frame) #frame object used only to cancel refreshing, I know it's stupid
        button_frame = Frame(master=self.main_frame, background="#f0f0f0")
        button_frame.grid(row=1, column=0, pady=20)

        main_button = Button(master=button_frame, text= "Main", font = ("Arial", 10), command = self.main_button, width=10)
        main_button.grid(row=0,column=0, pady=20)

        dc_button = Button(master=button_frame, text= "DC", font = ("Arial", 10), command = self.DC_monitoring, width=10)
        dc_button.grid(row=0,column=1, pady=20)

        ac_button = Button(master=button_frame, text= "AC", font = ("Arial", 10), command = self.AC_monitoring, width=10)
        ac_button.grid(row=0,column=2, pady=20, ipadx= 5)


        self.back_button = Button(master=button_frame, text= "Main menu", font = ("Arial", 10), command = self.back, width=10)
        self.back_button.grid(row=1,column=1)

        
        self.update_monitoring_data_1()

    def generate_others_menu(self):
        self.slave_address = 3
        self.main_frame.configure(padx=20, pady=20)
        button_grid = Frame(master=self.main_frame, bg="#f0f0f0")
        button_grid.grid(row=0, column=0)
        
        modbus_address_frame = Frame(master=button_grid, bg="#f0f0f0")
        modbus_address_frame.grid(row=0, column=0, columnspan=2, pady=5, padx=2.5)
        
        self.modbus_label = Label(master= modbus_address_frame, text=("Input slave device address: (current: " +  str(self.slave_address) +")"), bg="#f0f0f0")
        self.modbus_label.grid(row=0, column=0, pady=5, padx=2.5)
        
        slave_address_entry = Entry(master=modbus_address_frame, font = ("Arial", 10), relief=GROOVE, borderwidth=3)
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
        
        custom_register_frame = Frame(master= button_grid, bg="white", borderwidth=3, relief=GROOVE)
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
        
        
        self.output_box = Text(master=self.main_frame, width=50, state="disabled", relief=GROOVE, borderwidth=3)
        self.output_box.grid(row=0, column=1, pady=0)
        clear_button = Button(master=self.main_frame, text="Clear output console", font = ("Arial", 10), command=self.clear_output_console, width=30)
        clear_button.grid(row=1, column=1, pady=5, padx=2.5)
        
        self.back_button = Button(master=button_grid, text= "Main Menu", font = ("Arial", 10), command = self.back)   
        self.back_button.grid(row=5,column=0, columnspan=3, pady=20)
    
    def cancel_refresh(self):
        self.monitoring_frame.destroy()
        
    def close(self):
        self.main_window.destroy()    
    
    def back(self):
        self.main_frame.destroy()
        self.main_frame = Frame(master= self.main_window, bg="#f0f0f0")
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
            self.output_box.insert("end", "Warning code: "+ str(self.client.read_warning_message(self.slave_address)) + "\n")
        except:
            self.output_box.insert("end", "Connection failure\n")
        self.output_box.configure(state="disabled")       

    def read_measurments(self):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", "###########\n")
        try:
            #PV voltage
            pv_voltage = self.client.read_dc_voltage(self.slave_address)
            self.output_box.insert("end", "\nMPPT Voltage: \n")
            self.output_box.insert("end", "MPPT1 (V): " + str(pv_voltage[0]) + "MPPT2 (V): " + str(pv_voltage[1]) + "MPPT3 (V): " + str(pv_voltage[2] + "MPPT4 (V): " + str(pv_voltage[3])) + "MPPT5 (V): " + str(pv_voltage[4])+ "\n")
            self.output_box.insert("end", "MPPT6 (V): " + str(pv_voltage[5]) + "MPPT7 (V): " + str(pv_voltage[6]) + "MPPT8 (V): " + str(pv_voltage[7] + "MPPT9 (V): " + str(pv_voltage[8])) + "MPPT10 (V): " + str(pv_voltage[9]))
            del pv_voltage
            
            #PV current
            pv_current = self.client.read_dc_current(self.slave_address)
            self.output_box.insert("end", "\nMPPT Current: \n")
            self.output_box.insert("end", "MPPT1 (A): " + str(pv_current[0]) + "MPPT2 (A): " + str(pv_current[1]) + "MPPT3 (A): " + str(pv_current[2] + "MPPT4 (A): " + str(pv_current[3])) + "MPPT5 (A): " + str(pv_current[4])+ "\n")
            self.output_box.insert("end", "MPPT6 (A): " + str(pv_current[5]) + "MPPT7 (A): " + str(pv_current[6]) + "MPPT8 (A): " + str(pv_current[7] + "MPPT9 (A): " + str(pv_current[8])) + "MPPT10 (A): " + str(pv_current[9]))
            del pv_current

            #String current
            pv_current = self.client.read_string_current(self.slave_address)
            self.output_box.insert("end", "\nMPPT Current: \n")
            self.output_box.insert("end", "String 1 (A): " + str(pv_current[0]) + "String 2 (A): " + str(pv_current[1]) + "String 3 (A): " + str(pv_current[2] + "String 4 (A): " + str(pv_current[3])) + "String 5 (A): " + str(pv_current[4])+ "\n")
            self.output_box.insert("end", "String 6 (A): " + str(pv_current[5]) + "String 7 (A): " + str(pv_current[6]) + "String 8 (A): " + str(pv_current[7] + "String 9 (A): " + str(pv_current[8])) + "String 10 (A): " + str(pv_current[9])+ "\n")
            self.output_box.insert("end", "String 11 (A): " + str(pv_current[10]) + "String 12 (A): " + str(pv_current[11]) + "String 13 (A): " + str(pv_current[12] + "String 14 (A): " + str(pv_current[13])) + "String 15 (A): " + str(pv_current[14])+ "\n")
            self.output_box.insert("end", "String 16 (A): " + str(pv_current[15]) + "String 17 (A): " + str(pv_current[16]) + "String 18 (A): " + str(pv_current[17] + "String 19 (A): " + str(pv_current[18])) + "String 20 (A): " + str(pv_current[19]))
            del pv_current

            #AC voltage
            ac_voltage = self.client.read_ac_voltage(self.slave_address)
            self.output_box.insert("end", "\nAC Voltage: \n")
            self.output_box.insert("end", "L1: (V)" + str(ac_voltage["L1"]) + "L2 (V): " + str(ac_voltage["L2"]) + "L2 (V): " + str(ac_voltage["L3"]))
            del ac_voltage

            #Bus voltage
            self.output_box.insert("end", "Grid frequency (Hz): " + str(self.client.read_grid_freq(self.slave_address)) + "\n")
            
            #AC current
            ac_current = self.client.read_ac_current(self.slave_address)
            self.output_box.insert("end", "AC Current: \n")
            self.output_box.insert("end", "L1: (A)" + str(ac_current["L1"]) + "L2 (A): " + str(ac_current["L2"]) + "L2 (A): " + str(ac_current["L3"]))
            del ac_current

            #Internal temp
            self.output_box.insert("end", "Internal temp (C): " + str(self.client.read_internal_temp(self.slave_address)) + "\n")

            #Bus voltage
            self.output_box.insert("end", "Bus voltage (V): " + str(self.client.read_bus_voltage(self.slave_address)) + "\n")

            #Active power
            self.output_box.insert("end", "Active power (W): " + str(self.client.read_active_power(self.slave_address)) + "\n")

            #Apparent power
            self.output_box.insert("end", "Apparent power (VA): " + str(self.client.read_apparent_power(self.slave_address)) + "\n")

            #Reactive power
            self.output_box.insert("end", "Apparent power (Var): " + str(self.client.read_reactive_power(self.slave_address)) + "\n")

            #Power factor
            self.output_box.insert("end", "Power factor: " + str(self.client.read_power_factor(self.slave_address)) + "\n")
        except:
            self.output_box.insert("end", "Connection failure\n")
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
        
    def main_button(self):
        self.cancel_refresh()
        self.Simple_monitoring_button()

    def AC_monitoring(self):
        self.cancel_refresh()
        self.delete_all_onscreen_widgets()

        self.data_frame = Frame(master = self.main_frame, background="white", relief=GROOVE, borderwidth=3)
        self.data_frame.grid(row=0,column=0, ipady=5)

        title_label_1 = Label(master= self.data_frame, text="AC Voltage (V)", font = ("Arial", 12), bg="white")
        title_label_2 = Label(master= self.data_frame, text="AC Current (A)", font = ("Arial", 12), bg="white")
        title_label_3 = Label(master= self.data_frame, text="AC Frequency (Hz)", font = ("Arial", 12), bg="white")
        V_label = Label(master= self.data_frame, text="dddddddddddddddddddddddddddddddddddddddddddddddd", font = ("Arial", 10), bg="white")
        A_label = Label(master= self.data_frame, text="dddddddddddddddddddddddddddddddddddddddddddddddd", font = ("Arial", 10), bg="white")
        HZ_label = Label(master= self.data_frame, text="dddddddddddddddddddddddddddddddddddddddddddddddd", font = ("Arial", 10), bg="white")

        title_label_1.grid(row=0, column=0,ipadx=20,ipady=5)
        V_label.grid(row=1, column=0,ipadx=20,ipady=5)

        title_label_2.grid(row=2, column=0,ipadx=20,ipady=5)
        A_label.grid(row=3, column=0,ipadx=20,ipady=5)

        title_label_3.grid(row=4, column=0,ipadx=20,ipady=5)
        HZ_label.grid(row=5, column=0,ipadx=20,ipady=5)

        
        self.monitoring_frame = Frame(master=self.main_frame) #frame object used only to cancel refreshing, I know it's stupid
        button_frame = Frame(master=self.main_frame, background="#f0f0f0")
        button_frame.grid(row=1, column=0, pady=20)

        main_button = Button(master=button_frame, text= "Main", font = ("Arial", 10), command = self.main_button, width=10)
        main_button.grid(row=0,column=0, pady=20)

        dc_button = Button(master=button_frame, text= "DC", font = ("Arial", 10), command = self.DC_monitoring, width=10)
        dc_button.grid(row=0,column=1, pady=20)

        ac_button = Button(master=button_frame, text= "AC", font = ("Arial", 10), command = self.AC_monitoring, width=10)
        ac_button.grid(row=0,column=2, pady=20, ipadx= 5)


        self.back_button = Button(master=button_frame, text= "Main menu", font = ("Arial", 10), command = self.back, width=10)
        self.back_button.grid(row=1,column=1)
        
        self.update_monitoring_data_3()

    def DC_monitoring(self):
        
        self.cancel_refresh()
        self.delete_all_onscreen_widgets()

        self.data_frame = Frame(master = self.main_frame, background="white", relief=GROOVE, borderwidth=3)
        self.data_frame.grid(row=0,column=0, ipady=5)

        title_label_1 = Label(master= self.data_frame, text="PV Voltage (V)", font = ("Arial", 12), bg="white")
        title_label_2 = Label(master= self.data_frame, text="PV Current (A)", font = ("Arial", 12), bg="white")
        V_label_1 = Label(master= self.data_frame, text="dddddddddddddddddddddddddddddddddddddddddddddddd", font = ("Arial", 10), bg="white")
        V_label_2 = Label(master= self.data_frame, text="dddddddddddddddddddddddddddddddddddddddddddddddd", font = ("Arial", 10), bg="white")
        A_label_1 = Label(master= self.data_frame, text="dddddddddddddddddddddddddddddddddddddddddddddddd", font = ("Arial", 10), bg="white")
        A_label_2 = Label(master= self.data_frame, text="dddddddddddddddddddddddddddddddddddddddddddddddd", font = ("Arial", 10), bg="white")
        title_label_1.grid(row=0, column=0,ipadx=20,ipady=5)
        V_label_1.grid(row=1, column=0,ipadx=20,ipady=5)
        V_label_2.grid(row=2, column=0,ipadx=20,ipady=5)

        title_label_2.grid(row=3, column=0,ipadx=20,ipady=5)
        A_label_1.grid(row=4, column=0,ipadx=20,ipady=5)
        A_label_2.grid(row=5, column=0,ipadx=20,ipady=5)

        
        self.monitoring_frame = Frame(master=self.main_frame) #frame object used only to cancel refreshing, I know it's stupid
        button_frame = Frame(master=self.main_frame, background="#f0f0f0")
        button_frame.grid(row=1, column=0, pady=20)

        main_button = Button(master=button_frame, text= "Main", font = ("Arial", 10), command = self.main_button, width=10)
        main_button.grid(row=0,column=0, pady=20)

        dc_button = Button(master=button_frame, text= "DC", font = ("Arial", 10), command = self.DC_monitoring, width=10)
        dc_button.grid(row=0,column=1, pady=20)

        ac_button = Button(master=button_frame, text= "AC", font = ("Arial", 10), command = self.AC_monitoring, width=10)
        ac_button.grid(row=0,column=2, pady=20, ipadx= 5)


        self.back_button = Button(master=button_frame, text= "Main menu", font = ("Arial", 10), command = self.back, width=10)
        self.back_button.grid(row=1,column=1)
        
        self.update_monitoring_data_2()

    def update_monitoring_data_1(self):
        #TODO PROBABLY NEED TO CHANGE THE WAY DATA IS BEING REFRESHED, good enough for now: its 2AM
        self.data_frame.update_idletasks()
        print("UPDATING DATA")
        to_update = self.data_frame.winfo_children()
        to_update[0]["text"] = "SN: " + "LM08K09S22503221" + ", Model: " + "ASW8KH-T1"
        to_update[1]["text"] = "Device state: " + "normal"
        to_update[2]["text"] = "Active power: " + str(randint(500,700))
        to_update[3]["text"] = "E-today: " + str(randint(3,10))
        to_update[4]["text"] = "E-total: " + str(randint(33,700))
        to_update[5]["text"] = "Error code: " + str(randint(0,99))
        
        self.monitoring_frame.after(3000, self.update_monitoring_data_1)

    def update_monitoring_data_2(self):
        self.data_frame.update_idletasks()
        print("UPDATING DATA PV")
        to_update = self.data_frame.winfo_children()
        to_update[2]["text"] = "PV1: " + str(randint(1000,2000)) + "   PV2: " + str(randint(1000,2000)) + "   PV3: " + str(randint(1000,2000)) + "   PV4: " + str(randint(1000,2000)) + "   PV5: " + str(randint(1000,2000))
        to_update[3]["text"] = "PV6: " + str(randint(1000,2000)) + "   PV7: " + str(randint(1000,2000)) + "   PV8: " + str(randint(1000,2000)) + "   PV9: " + str(randint(1000,2000)) + "   PV10: " + str(randint(1000,2000))
        to_update[4]["text"] = "PV1: " + str(randint(1000,2000)) + "   PV2: " + str(randint(1000,2000)) + "   PV3: " + str(randint(1000,2000)) + "   PV4: " + str(randint(1000,2000)) + "   PV5: " + str(randint(1000,2000))
        to_update[5]["text"] = "PV6: " + str(randint(1000,2000)) + "   PV7: " + str(randint(1000,2000)) + "   PV8: " + str(randint(1000,2000)) + "   PV9: " + str(randint(1000,2000)) + "   PV10: " + str(randint(1000,2000))

        self.monitoring_frame.after(3000, self.update_monitoring_data_2)

    def update_monitoring_data_3(self):
        self.data_frame.update_idletasks()
        print("UPDATING DATA AC")
        to_update = self.data_frame.winfo_children()
        to_update[3]["text"] = "L1: " + str(randint(230,250)) + "   L2: " + str(randint(230,250)) + "   L3: " + str(randint(230,250))
        to_update[4]["text"] = "L1: " + str(randint(0,5)) + "   L2: " + str(randint(0,10)) + "   L3: " + str(randint(0,7))
        to_update[5]["text"] = "Frequency: " + str(randint(49,51))

        self.monitoring_frame.after(3000, self.update_monitoring_data_3)
    
SimpleGui()