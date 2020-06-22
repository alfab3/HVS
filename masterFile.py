#masterFile for HVS
#Written by Albert Fabrizi
#Version: June 18, 2020 12:55

from Tkinter import *
import Tkinter as tk
import time
import voltage_ramp
from voltage_ramp import voltageRampCheck, voltage_ramp_up, voltage_ramp_down
import random

mainWindow = Tk()

class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self,master)

        self.master = master

        self.init_window()#main window and menu bar

        self.main_widgets()#objects that inhabit the main page

        #conversions
        self.voltageConversion = 300 * 1800 / 1709
        self.currentConversion = 3.3/100

    #use this function for menu bar and page title
    def init_window(self):
        self.master.title('HVS')

        #cascade menus
        menu = Menu(mainWindow)
        mainWindow.config(menu = menu)

        #file cascade menu
        file_C = Menu(menu)
        file_C.add_command(label='Exit', command = self.close_window)
        menu.add_cascade(label='File', menu=file_C)

    #this function defines the main page controls
    def main_widgets(self):
        #ramp voltage entry
        Label(mainWindow, text='Enter Desired Voltage: ').grid(row = 0)
        #voltage entry user input
        self.v_Entry = Entry(mainWindow)
        self.v_Entry.grid(row = 0, column = 1)

        #Button to pass entry to ramp voltage function
        v_Activate = Button(mainWindow, text='Enter', command=self.ramp_Entry_Check)
        v_Activate.grid(row = 0, column = 2)


    #voltage ramp function
    def r_Entry(self, goalVoltage):

        ramp_up = False
        ramp_down = False

        #Get values of voltage and current
        voltage, current = voltageRampCheck()


        if goalVoltage > voltage:
            voltage_ramp_up(goalVoltage)
            ramp_up = True
        else:
            voltage_ramp_down(goalVoltage)
            ramp_down = True
        
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
            except:
                check = False
        if check == True:
            self.r_Entry(rampV)


    #individual menu functions
    def close_window(self):
        exit()

#intial size of window
mainWindow.geometry('600x300')
app = Window(mainWindow)

#mainloop stays at the end
mainWindow.mainloop()
