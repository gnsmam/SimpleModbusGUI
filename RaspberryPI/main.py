#! /usr/bin/env
from Solplanet_serial_modbus import Solplanet_Serial_Modbus
from tkinter import *
from customtkinter import *
from time import sleep

from random import randint ## for testing purposes (see refresh_monitoring_data method)

class CButton(CTkButton):
    def __init__(self, text, master, command, width = 70, height = 30):
        super().__init__(master = master, width = width, height = height, text = text, font= ("Arial", 15), fg_color="#33383f", command = command, anchor=CENTER, border_width=2, border_color="white")

class CLabel(CTkLabel):
    def __init__(self, master, font= ("Arial", 15), pady = 5, padx = 25, textvariable = "", text = ""):
        super().__init__(master = master, text = text, font = font, fg_color = "#33383f", text_color = "white", padx = padx, pady = pady, textvariable = textvariable)

class CEntry (CTkEntry):
    def __init__(self, master, textvariable):
        super().__init__(master = master, textvariable = textvariable, border_width=2, border_color="white" )

class SimpleGui(): 
    def __init__(self):
         
        self.main_window = Tk() #instance of windows class
        #self.main_window.attributes('-fullscreen', True)
        self.port = StringVar()
        self.slave_address = StringVar()
        self.backup_address = StringVar()
        self.main_window.minsize(480,320)
        self.main_window.maxsize(480,320)
        self.main_window.title("SimpleModbus")
        self.main_window.configure(background="#33383f")
        self.main_frame = Frame(master= self.main_window, bg="#33383f")
        self.main_frame.pack(expand=True)

        self.input_window_startup()

        self.main_window.mainloop() #place window, listen for events 
    
    def input_window_startup(self):
        
        self.delete_all_onscreen_widgets()

        self.port = StringVar()
        self.slave_address = StringVar()
        self.backup_address = StringVar()

        port_label = CLabel(master= self.main_frame, text = "Input RS communication port:")
        port_entry = CEntry(master=self.main_frame, textvariable = self.port)
        modbus_label = CLabel(master= self.main_frame, text = "Input Device Modbus Address (for monitoring functionality):")
        modbus_entry = CEntry(master=self.main_frame, textvariable = self.slave_address)
        save_button = CButton(master=self.main_frame, text="Save", command = lambda: self.set_startup_parameters(port = port_entry, address = modbus_entry))

        port_label.grid(row=0, column=0)
        port_entry.grid(row=2, column=0)
        modbus_label.grid(row=3, column=0)
        modbus_entry.grid(row=5, column=0)

        save_button.grid(row=6, column=0, pady=10)

    def set_startup_parameters(self, port, address):
        self.slave_address = int(self.slave_address.get())
        self.backup_address = self.slave_address
        self.port = self.port.get()

        self.client = Solplanet_Serial_Modbus(s_port = self.port)

        self.generate_main_menu()

    def generate_main_menu(self):
        self.slave_address = self.backup_address
        print(self.port)
        print(self.slave_address)

        self.delete_all_onscreen_widgets()
        button1 = CButton(master=self.main_frame, text="Simple Monitoring", command=self.Simple_monitoring_button, width=200)
        button2 = CButton(master=self.main_frame,  text="Settings", command=self.input_window_startup, width=200) 
        button1.grid(row=0, column=0, pady=5)
        button2.grid(row=1, column=0, pady=5)
        close_button = CButton(master=self.main_frame, text= "Exit", command = self.close, width=200)
        close_button.grid(row=3, column=0, pady=5)     

    def Simple_monitoring_button(self):
        self.delete_all_onscreen_widgets()
        self.monitoring_menu_1()
        
    def delete_all_onscreen_widgets(self):
        to_delete = self.main_frame.grid_slaves()
        for widget in to_delete:
            widget.destroy()    

    def monitoring_menu_1(self):
        self.monitoring_frame = Frame(master=self.main_frame) #frame object used only to cancel refreshing, I know it's stupid

        self.sn = StringVar()
        self.model = StringVar()
        self.state = StringVar()
        self.active_power = StringVar()
        self.e_today = StringVar()
        self.e_total = StringVar()
        self.error = StringVar()

        self.data_frame = Frame(master = self.main_frame, background="#33383f")
        self.data_frame.grid(row=0,column=0)

        sn_label = CLabel(master = self.data_frame, textvariable = self.sn)
        model = CLabel(master = self.data_frame, textvariable = self.model) 
        device_state_label = CLabel(master = self.data_frame, textvariable = self.state)
        active_power_label = CLabel(master = self.data_frame, textvariable = self.active_power)
        e_today_label = CLabel(master = self.data_frame, textvariable = self.e_today)
        e_total_label = CLabel(master = self.data_frame, textvariable = self.e_total)
        error_code_label = CLabel(master=self.data_frame, textvariable=self.error)
        
        sn_label.grid(row = 0, column = 1, sticky = E)
        model.grid(row = 1, column = 1, sticky = E)
        device_state_label.grid(row = 2, column = 1, sticky = E)
        active_power_label.grid(row = 3, column = 1, sticky = E)
        e_today_label.grid(row = 4, column = 1, sticky = E)
        e_total_label.grid(row = 5, column = 1, sticky = E)
        error_code_label.grid(row = 6, column = 1, sticky = E)

        label_1 = CLabel(master= self.data_frame, text = "SN: ")
        label_1.grid(row=0, column=0, sticky = W)
        label_2 = CLabel(master= self.data_frame, text = "Model: ")
        label_2.grid(row=1, column=0, sticky = W)
        label_3 = CLabel(master= self.data_frame, text = "Device Status: ")
        label_3.grid(row=2, column=0, sticky = W)
        label_4 = CLabel(master= self.data_frame, text = "Active Power: ")
        label_4.grid(row=3, column=0, sticky = W)
        label_5 = CLabel(master= self.data_frame, text = "E-Today: ")
        label_5.grid(row=4, column=0, sticky = W)
        label_6 = CLabel(master= self.data_frame, text = "E-Total: ")
        label_6.grid(row=5, column=0, sticky = W)
        label_7 = CLabel(master= self.data_frame, text = "Current Error Code: ")
        label_7.grid(row=6, column=0, sticky = W)
               
        self.create_button_menu()
        self.update_monitoring_data_1() 

    def cancel_refresh(self):
        self.monitoring_frame.destroy()
        
    def close(self):
        self.main_window.destroy()    
    
    def back(self):
        self.main_frame.destroy()
        self.main_frame = Frame(master= self.main_window, bg="#33383f")
        self.generate_main_menu()
        self.main_frame.pack(expand=True)
        self.delete_useless()    
        
    def delete_useless(self):
        try:
            del self.sn 
            del self.model 
            del self.state 
            del self.active_power 
            del self.e_today 
            del self.e_total
            del self.error 
        except:
            print("nothing to delete > Main")  

        try:
            del self.dc_a_1
            del self.dc_a_2
            del self.dc_v_1
            del self.dc_v_2
        except:
            print("nothing to delete > DC")

        try:
            del self.ac_v 
            del self.ac_a 
            del self.ac_hz 

        except:
            print("nothing to delete > AC")

    def main_button(self):
        self.cancel_refresh()
        self.delete_useless()
        self.Simple_monitoring_button()

    def AC_monitoring(self):
        self.cancel_refresh()
        self.delete_useless()
        self.delete_all_onscreen_widgets()

        self.data_frame = Frame(master = self.main_frame, background="#33383f")
        self.data_frame.grid(row=0,column=0)

        self.ac_v = StringVar()
        self.ac_a = StringVar()
        self.ac_hz = StringVar()

        title_label_1 = CLabel(master= self.data_frame, text="AC Voltage (V)")
        title_label_2 = CLabel(master= self.data_frame, text="AC Current (A)")
        title_label_3 = CLabel(master= self.data_frame, text="AC Frequency (Hz)")
        V_label = CLabel(master= self.data_frame, textvariable = self.ac_v)
        A_label = CLabel(master= self.data_frame, textvariable = self.ac_a)
        HZ_label = CLabel(master= self.data_frame, textvariable = self.ac_hz)

        title_label_1.grid(row=0, column=0)
        V_label.grid(row=1, column=0)

        title_label_2.grid(row=2, column=0)
        A_label.grid(row=3, column=0)

        title_label_3.grid(row=4, column=0)
        HZ_label.grid(row=5, column=0)

        
        self.monitoring_frame = Frame(master=self.main_frame) #frame object used only to cancel refreshing, I know it's stupid
        
        self.create_button_menu()
        
        self.update_monitoring_data_3()

    def DC_monitoring(self):
        self.cancel_refresh()
        self.delete_useless()
        self.delete_all_onscreen_widgets()

        self.dc_v_1 = StringVar()
        self.dc_a_1 = StringVar()
        self.dc_v_2 = StringVar()
        self.dc_a_2 = StringVar()

        self.data_frame = Frame(master = self.main_frame, background="#33383f")
        self.data_frame.grid(row=0,column=0, ipady=5)

        title_label_1 = CLabel(master= self.data_frame, text="PV Voltage (V)")
        title_label_2 = CLabel(master= self.data_frame, text="PV Current (A)")
        V_label_1 = CLabel(master= self.data_frame, textvariable = self.dc_v_1)
        V_label_2 = CLabel(master= self.data_frame, textvariable = self.dc_v_2)
        A_label_1 = CLabel(master= self.data_frame, textvariable = self.dc_a_1)
        A_label_2 = CLabel(master= self.data_frame, textvariable = self.dc_a_2)
        title_label_1.grid(row=0, column=0)
        V_label_1.grid(row=1, column=0)
        V_label_2.grid(row=2, column=0)

        title_label_2.grid(row=3, column=0)
        A_label_1.grid(row=4, column=0)
        A_label_2.grid(row=5, column=0)

        
        self.monitoring_frame = Frame(master=self.main_frame) #frame object used only to cancel refreshing, I know it's stupid
        self.create_button_menu()

        self.update_monitoring_data_2()

    def update_monitoring_data_1(self):   
        print("UPDATING DATA - MAIN")
        
        self.sn.set("N/A")
        self.model.set("N/A")
        self.state.set("N/A")
        self.active_power.set("N/A")
        self.e_today.set("N/A")
        self.e_total.set("N/A")
        self.error.set("N/A")
            
        self.main_window.update_idletasks()
        
        self.data_frame.after(4000, self.update_monitoring_data_1)

    def update_monitoring_data_2(self):
        
        print("UPDATING DATA PV")
        #voltage
        try:
            pv_voltage = self.client.read_dc_voltage(self.slave_address)
        except:
            pv_voltage = ["N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]

        self.dc_v_1.set("PV1: " + str(pv_voltage[0]) + "   PV2: " + str(pv_voltage[1]) + "   PV3: " + str(pv_voltage[2]) + "   PV4: " + str(pv_voltage[3]) + "   PV5: " + str(pv_voltage[4]))
        self.dc_v_2.set("PV6: " + str(pv_voltage[5]) + "   PV7: " + str(pv_voltage[6]) + "   PV8: " + str(pv_voltage[7]) + "   PV9: " + str(pv_voltage[8]) + "   PV10: " + str(pv_voltage[9]))
        del pv_voltage
        
        #current
        try:
            pv_current = self.client.read_dc_current(self.slave_address)
        except:
            pv_current = ["N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]

        self.dc_a_1.set("PV1: " + str(pv_current[0]) + "   PV2: " + str(pv_current[1]) + "   PV3: " + str(pv_current[2]) + "   PV4: " + str(pv_current[3]) + "   PV5: " + str(pv_current[4]))
        self.dc_a_2.set("PV6: " + str(pv_current[5]) + "   PV7: " + str(pv_current[6]) + "   PV8: " + str(pv_current[7]) + "   PV9: " + str(pv_current[8]) + "   PV10: " + str(pv_current[9]))
        del pv_current
        self.data_frame.update_idletasks()
        self.monitoring_frame.after(4000, self.update_monitoring_data_2)

    def update_monitoring_data_3(self):
        print("UPDATING DATA AC")
        try: 
            ac_voltage = self.client.read_ac_voltage(self.slave_address)
        except:
            ac_voltage = {"L1" : "N/A", "L2" : "N/A", "L3" : "N/A"}
        
        self.ac_v.set("L1: " + str(ac_voltage["L1"]) + "   L2: " + str(ac_voltage["L2"]) + "   L3: " + str(ac_voltage["L3"]))
        del ac_voltage

        try: 
            ac_current = self.client.read_ac_current(self.slave_address)
        except:
            ac_current = {"L1" : "N/A", "L2" : "N/A", "L3" : "N/A"}

        self.ac_a.set("L1: " + str(ac_current["L1"]) + "   L2: " + str(ac_current["L2"]) + "   L3: " + str(ac_current["L3"])) 
        del ac_current

        try:
            freq = self.client.read_grid_freq(self.slave_address)
        except:
            freq = "N/A"
        self.ac_hz.set(str(freq))

        self.monitoring_frame.after(4000, self.update_monitoring_data_3)
        self.data_frame.update_idletasks()
    
    def create_button_menu(self):
        button_frame = Frame(master=self.main_frame, background="#33383f")
        button_frame.grid(row=1, column=0)

        main_button = CButton(master=button_frame, text= "Main", command = self.main_button, width=95)
        main_button.grid(row=0,column=0,pady=10, padx=5)

        dc_button = CButton(master=button_frame, text= "DC", command = self.DC_monitoring, width=95)
        dc_button.grid(row=0,column=1,pady=10, padx=5)

        ac_button = CButton(master=button_frame, text= "AC", command = self.AC_monitoring, width=95)
        ac_button.grid(row=0,column=2,pady=10, padx=5)

        self.back_button = CButton(master=button_frame, text= "Main Menu", command = self.back, width=95)
        self.back_button.grid(row=1,column=1)
SimpleGui()
