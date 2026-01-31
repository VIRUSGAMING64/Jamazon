from customtkinter import *
from CTkMessagebox import CTkMessagebox
from modules.events import *
from modules.utils import *
from modules.gvar import *

class parameter:
    data = None
    def call(self):
        ev_info = format_event_info(self.data)
        CTkMessagebox(title="Event Information", message=ev_info)

    def call2(self):
        s = ""
        if self.data == None:
            s = "Can be used with all resources"
        else:
            for i in self.data:
                s += " " + str(i)
        titl = "Not use with"
        if s == "":
            titl = "Usable" 
            s = "Usable with any resource"
        CTkMessagebox(title=titl, message=s)


class EventShower(CTkToplevel):
    def __init__(self, event_list:list[event] = []):
        super().__init__()
        self.after(1001, self.lift)
        self.resizable(False, False)
        self.title("event shower")
        self.geometry("600x500")

        self.scrollable_frame = CTkScrollableFrame(master=self, width=200, height=300, label_text="events running")
        self.scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.buttons = []
        
        for i in range(len(event_list)):
            data = parameter()
            data.data = event_list[i]
            item = CTkButton(
                master=self.scrollable_frame, 
                text=f"{i} - {event_list[i].task}  {event_list[i].date[0]} TO {event_list[i].date[1]}", 
                command=data.call
            )
            item.pack(pady = 2)
            self.buttons.append([item,data])

        self.horizontal_frame = CTkScrollableFrame(master=self, orientation="horizontal", height=50)
        self.horizontal_frame.pack(pady=10, fill="x")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.destroy()


class ResourceShower(CTkToplevel):
    def __init__(self, res:list[event] = []):
        super().__init__()
        self.after(100, self.lift) 
        self.resizable(False, False)
        self.title("Resource shower")
        self.geometry("600x500")
        
        self.scrollable_frame = CTkScrollableFrame(master=self, width=200, height=300, label_text="All available resources")
        self.scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.buttons = []

        for res in calendar.resources:
            not_need = calendar.resources[res]["without"]
            data = parameter()
            data.data = not_need
            item = CTkButton(
                master=self.scrollable_frame, 
                text=f"{res}:  {calendar.resources[res]["count"]}", 
                command=data.call2
            )
            item.pack(pady=2, padx=2)
            self.buttons.append([item,data])

        self.horizontal_frame = CTkScrollableFrame(master=self, orientation="horizontal", height=50)
        self.horizontal_frame.pack(pady=10, fill="x")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.destroy()