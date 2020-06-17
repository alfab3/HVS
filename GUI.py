#GUI for the HVS
#Written by Albert Fabrizi and Gregory Turnberg
#Please update the date and time here so we can keep track of the newest copy:
#Version: June 16, 2020 13:13
#TODO:
#3b)Prep for hardware test
#5)Format py file to executable - last step
from Tkinter import *
import Tkinter as tk
import time
import voltage_ramp
from voltage_ramp import voltageRampInit, voltage_ramp_up, voltage_ramp_down
import random

mainWindow = Tk()
#master window class

class Window(Frame):
    def __init__(self,master = None):
        Frame.__init__(self,master)

        self.master = master

        self.init_window()#main window and menu bar

        self.main_widgets()#objects that inhabit the main page
        
        #Conversion ratios derived by Dan
        self.voltageConversion = 300 * 1800 / 1709
        self.currentConversion = 3.3/10

    #use this function for menu bar and page title
    def init_window(self):
        self.master.title('HVS')

        #cascade menus
        #this only works if you keep the variable name as "menu"
        menu = Menu(mainWindow)
        mainWindow.config(menu = menu)
        #all menu functions require the command passed from a seperate function
        #file cascade menu 
        file_C = Menu(menu)
        file_C.add_command(label='Exit', command=self.close_window)
        menu.add_cascade(label='File', menu=file_C)

#this function defines the main page controls
    def main_widgets(self):
        #ramp voltage entry
        Label(mainWindow, text='Enter Desired Voltage: ').grid(row = 0)
        #Voltage Entry user input
        self.v_Entry = Entry(mainWindow)
        self.v_Entry.grid(row = 0, column = 1)
        
        #Button to pass entry to ramp voltage function, as to not cause lag
        v_Activate = Button(mainWindow, text='Enter', command=self.ramp_Entry_Check)
        v_Activate.grid(row = 0, column = 2)
        
        #Text box that will read out what used to be printed to console 
        self.text_box = Text(mainWindow,height=15,width=45)
        self.text_box.grid(row=3,column=1)
        self.text_box.insert(tk.INSERT,'-----\n\n')
        self.text_box.configure(state='disabled')


#voltage ramp function
    def r_Entry(self, goalVoltage):

        #Get values of voltage and current
        voltage, current = voltageRampCheck()
        
        #check for ramp up or ramp down 
        if goalVoltage > voltage:
            voltage_ramp_up(goalVoltage)
            ramp_up = True
            ramp_down = False
        else:
            voltage_ramp_down(goalVoltage)
            ramp_down = True
            ramp_up = False

        #print initial values to textbox
        self.text_box.configure(state = 'normal')
        self.text_box.insert(tk.END,'Voltage start at ' + str(in_volt) + '...\n')
        self.text_box.insert(tk.END,'-----------\n')
        self.text_box.insert(tk.END,'Max Current Set to ' + str(in_cur) + '\n')
        self.text_box.insert(tk.END,'-----------\n')
        self.text_box.configure(state='disabled')

        #time functions to generate clock and update text box
        prevT = time.time()
        
        #if ramp up function is called the following loop starts
        while ramp_up == True:
            liveT = time.time()
            #to make sure there is a second between each clock
            if liveT - prevT < 1:
                continue
            #takes new readings every pass to print updated information
            voltage, current = voltageRampCheck()
            
            #update time:
            prevTime = livetime
            
            #print readings from ADC
            self.text_box.configure(state = 'normal')
            self.text_box.insert(tk.END, 'Voltage: ' + str(volt) + '\n')
            self.text_box.insert(tk.END, '-------------------\n')
            self.text_box.insert(tk.END, 'Max Current: ' + str(cur) + '\n')
            self.text_box.insert(tk.END, '-------------------\n')
            self.text_box.configure(state = 'disabled')
            
            #end printing if done or continue loop
            if volt > goalVoltage:
                ramp_up = False
                hold_value_print(goalVoltage)
            else:
                continue

        while ramp_down == True: #this loop mirrors the ramp up printing
            liveT = time.time()
            if liveT - prevT < 1:
                continue

            curReading = self.mcp328.take_single_reading(1)
            cur = curReading * self.currentConversion
            volReading = self.mcp3428.take_single_reading(0)
            volt = volReading * self.voltageConversion
            prevTime = livetime

            self.text_box.configure(state = 'normal')
            self.text_box.insert(tk.END, 'Voltage: ' + str(volt) + '\n')
            self.text_box.insert(tk.END, '-------------------\n')
            self.text_box.insert(tk.END, 'Max Current: ' + str(cur) + '\n')
            self.text_box.insert(tk.END, '-------------------\n')
            self.text_box.configure(state = 'disabled')

            if volt < goalVoltage:
                ramp_down = False
                hold_value_print(goalVoltage)
            else:
                continue

    def hold_value_print(self,goalVoltage):#prints the hold value parameters and information
        self.text_box.configure(state = 'normal')
        self.text_box.insert(tk.END, 'Bringing to ' + str(goalVoltage) + 'Volts.....')
        self.text_box.configure(state = 'disabled')
        while True:
            volt_check = self.mcp3428.take_single_reading(0)
            volts = volt_check * self.voltageConversion
            

            if volts < (goalVoltage - 1):
                self.text_box.configure(state = 'normal')
                self.text_box.insert(tk.END, 'Voltage: ' + str(self.mcp3428.take_single_reading(0) * voltageConversion))
                self.text_box.configure(state = 'disabled')
            elif volts > (goalVoltage + 1):
                self.text_box.configure(state = 'normal')
                self.text_box.insert(tk.END, 'Voltage: ' + str(self.mcp3428.take_single_reading(0) *voltageConversion))
                self.text_box.configure(state = 'disabled')
            else:
                continue
        
        
#this function will check if the entered value is an int, float, etc. then pass
#to voltage ramp function
    def ramp_Entry_Check(self):
        rampV = self.v_Entry.get()
        check = None
        try:#check if int
            rampV = int(rampV)
            check = True
        except:
            try:#check if float
                rampV = float(rampV)
                check = True
            except:#if the input is not a float or int, it fails
                self.text_box.configure(state='normal')#to add config must be turned on
                self.text_box.insert(tk.END,'Error: Entry must be an Integer or Float\n')
                self.text_box.insert(tk.END, '----------------\n')
                self.text_box.configure(state='disabled')#turned off to prevent user input in text box
                check = False
        if check == True:#check if voltage is in the desired range
            if rampV < 0 or rampV > 3000:
                self.text_box.configure(state='normal')
                self.text_box.insert(tk.END, 'Error: Entry must be between 0V and 3000V\n')
                self.text_box.insert(tk.END, '----------------\n')
                self.text_box.configure(state='disabled')
            else:
                self.r_Entry(rampV)#print entry voltage to text box
                self.text_box.configure(state='normal')
                self.text_box.insert(tk.END,'Voltage increasing to : ' + str(rampV) + '\n')
                self.text_box.insert(tk.END, '----------------\n')
                self.text_box.configure(state='disabled')        
#individual menu functions
    def close_window(self):
        exit()
#When ramp_Entry() is called with a valid voltage, print out info to text box
    def ramp_print_entry(self,voltage):
        self.text_box.configure(state='normal')
        self.text_box.insert(tk.END,'----------------\n')
        self.text_box.insert(tk.END,'Voltage (0 to 3000 V): ' + str(voltage) + '\n')
        self.text_box.insert(tk.END,'----------------\n')
        self.text_box.configure(state='disabled')

#initial size of window:
mainWindow.geometry('600x300')
app = Window(mainWindow)

#mainloop stays at the end
mainWindow.mainloop()
