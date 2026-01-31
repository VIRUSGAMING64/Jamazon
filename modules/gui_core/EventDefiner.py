from customtkinter import *
from modules.gvar import *
from modules.utils import *
from threading import Thread
from CTkMessagebox import CTkMessagebox


class EventCreator(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.after(100, self.lift)
        self.title("Create Event")
        self.geometry("400x300")
        self.res_name_entry = CTkEntry(self, placeholder_text="Resource names separated by ,", width= 200)
        self.res_name_entry.pack(pady=10)
        self.res_count_entry = CTkEntry(self, placeholder_text="Event name")
        self.res_count_entry.pack(pady=10)
        self.add_button = CTkButton(self, text="Add event", command=self.create_event_callback)
        self.add_button.pack(pady=20)
    

    def GetCounts(self, resource):
        print(resource)
        return 1
    

    def create_event(self,name:str,resources:list):
        if name in calendar.available_tasks:
            CTkMessagebox(self,200, 200 , title="Error", message=f"Event '{name}' already exists.")
            return False
        calendar.available_tasks[name] = {}
        calendar.available_tasks[name]["resources"] = []
        for res,count in resources:
            calendar.available_tasks[name]["resources"].append({
                "name": res,
                "count": count
            })
        calendar.available_tasks[name]["without"] = []
        calendar._save_tasks("./templates/tasks.json")
            

    def create_event_callback(self):
        res_names = self.res_name_entry.get().split(',')
        if "" in res_names:
            res_names.remove("")
        event_name = self.res_count_entry.get()
        if event_name == "" or len(res_names) == 0:
            CTkMessagebox(self,200, 200 , title="Error", message="Please enter a valid event name and resources.")
            return
        A = set()
        B = set()
        for res in res_names:
            if not res in calendar.resources:
                CTkMessagebox(self,200, 200 , title="Error", message=f"Resource '{res}' does not exist.")
                return
            deps = get_sources_dependency(calendar.resources, res)
            A.add(res)
            for d in deps:
                A.add(d)

        B = set()
        for resource in A:
            for el in calendar.resources[resource]["without"]:
                B.add(el)

        C = A & B
        print(A,B,C)
        if len(C) > 0:
            CTkMessagebox(self,200, 200 , title="Error", message=f"Resource collision detected: {', '.join(C)}\n remove this resource")
            print(A,B,C)
            return

        need = []
        for res in res_names:
            need.append([res,self.GetCounts(res)])

        if False == self.create_event(event_name, need):
            return
        
        CTkLabel(self, text="Event created successfully!").pack(pady=10)