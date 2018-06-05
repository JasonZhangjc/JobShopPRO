import tkinter as form
from tkinter import ttk
from tkinter import messagebox
from globalData import machinesList, STRGS
#=========================================================================================
class GuiTaskNew(form.Toplevel):
    """Form for adding new Task in itinerary"""

    def __init__(self, master, aNewTask):
        form.Toplevel.__init__(self, master)

        self.title(STRGS['TITLE_NEW_TASK_INITERARY'])
        self.geometry("%dx%d+%d+%d" % (200,150, int(self.winfo_screenwidth() / 2 - 200 / 2), int(self.winfo_screenheight() / 2 - 150 / 2)))
        self.resizable(False, False)

        frTaskNew = ttk.LabelFrame(self, text=STRGS['NEW_TASK'])
        frTaskNew.grid(column=0, row=0, padx=5, pady=5)

        ttk.Label(frTaskNew, text=STRGS['NAME']).grid(column=0, row=0, padx=3, pady=3, sticky=form.W)
        ttk.Label(frTaskNew, text=STRGS['DURATION']).grid(column=0, row=1, padx=3, pady=3, sticky=form.W)
        ttk.Label(frTaskNew, text=STRGS['MACH']).grid(column=0, row=2, padx=3, pady=3, sticky=form.W)

        self.entTaskNameVar = form.StringVar()
        self.entTaskName = ttk.Entry(frTaskNew, textvariable=self.entTaskNameVar, width=17)
        self.entTaskName.grid(column=1, row=0, padx=3, pady=3)
        self.entTaskName.focus()
        self.entTaskNameVar.set(aNewTask.name)

        self.entTaskDurationVar = form.DoubleVar()
        vcmd = (master.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entTaskDuration = ttk.Entry(frTaskNew, textvariable=self.entTaskDurationVar, width=17, validate='key', validatecommand = vcmd)
        self.entTaskDuration.grid(column=1, row=1, padx=3, pady=3)
        self.entTaskDurationVar.set(aNewTask.duration)

        #combobox that is filled with all names from machines list. it is also readonly so value must be selected
        self.choosenMachine = form.StringVar()
        self.cbMachine = ttk.Combobox(frTaskNew, width=14, textvariable=self.choosenMachine, state="readonly", values=[mach.name for mach in machinesList])
        self.cbMachine.current(aNewTask.machine.ID)           #first element is selected
        self.cbMachine.grid(column=1, row=2, padx=3, pady=3)

        #passing command with argument
        ttk.Button(self, text=STRGS['SAVE'], width=30, command=lambda: self.saveNewTask(aNewTask)).grid(column=0, row=1, pady=5, padx=5)
        
        #set to be on top, hijack all comands and pause anything until close
        self.transient(master)
        self.grab_set()
        master.wait_window(self)

    def saveNewTask(self, aNewTask):
        aNewTask.taskChanged = False
        if len(self.entTaskName.get()) != 0:
            if len(self.entTaskDuration.get()) != 0:
                if float(self.entTaskDuration.get()) > 0:
                    aNewTask.duration = float(self.entTaskDuration.get())
                    aNewTask.name = self.entTaskName.get()
                    global machinesList
                    aNewTask.machine = machinesList[self.cbMachine.current()]
                    aNewTask.taskChanged = True
                    self.destroy()
                else:
                    messagebox.showerror(STRGS['MSG_ERR_WRONG_VAL'], STRGS['MSG_ERR_TASK_CORRECT_DURATION'])
            else:
                messagebox.showerror(STRGS['MSG_ERR_WRONG_VAL'], STRGS['MSG_ERR_EMPTY_VAL'])
        else:
            messagebox.showerror(STRGS['MSG_ERR_ITINERARY_NO_NAME'], STRGS['MSG_ERR_ITINERARY_ENTER_NAME'])
        pass


    def validate(self, action, index, valueIfAllowed, priorValue, text, validationType, triggerType, widgetName):
        """ Preserve to enter only specified keys into entry """
        if(action == '1'): #user can delete input e.g. erase wrong number and enter it again
            if text in '0123456789.':
                try:
                    float(valueIfAllowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True