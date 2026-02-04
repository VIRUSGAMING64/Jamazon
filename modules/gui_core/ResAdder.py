from modules.gvar import *
from customtkinter import *
from CTkMessagebox import CTkMessagebox

class ResAdder(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.after(100, self.lift)  
        self.title("Add Resource")
        self.geometry("400x300")
        self.res_name_entry      = CTkEntry(self, placeholder_text="Resource Name")
        self.res_name_entry.pack(pady=10)
        self.res_count_entry     = CTkEntry(self, placeholder_text="Resource Count")
        self.res_count_entry.pack(pady=10)
        self.add_button          = CTkButton(self, text="Add Resource", command=self.add_resource_callback)
        self.add_button.pack(pady=20)


    def add_resource_callback(self):
        res_name        = self.res_name_entry.get()
        res_count: str  = (self.res_count_entry.get())
        flag            = 1

        if res_count.startswith("-"):
            res_count = res_count.removeprefix("-")
            flag = -1
  
        if (res_name == "") or (not res_count.isnumeric()):
            CTkMessagebox(self,200, 200 , title="Error", message="Please enter a valid resource name and count.")
            return
  
        res_count = int(res_count)
        res_count *= flag
        if self.add_resource(res_name, res_count) == False:
            return
        
        CTkLabel(self, text="Resource added successfully!").pack(pady=10)   
        self.add_button.configure(text="exit", command=self.destroy)
        

    def add_resource(self, res_name:str, inc:int, need:list = [], witout = []):
        if not (res_name in calendar.resources):
            if inc <= 0:
                CTkMessagebox(self,200, 200 , title="Error", message="Please enter a valid resource name and count.")
                return False
            calendar.resources[res_name] = {}
            calendar.resources[res_name]["count"] = inc
            calendar.resources[res_name]["need"] = need
            calendar.resources[res_name]["without"] = witout
        else:
            if calendar.resources[res_name]["count"] < abs(inc) and inc:
                CTkMessagebox(self,200, 200 , title="Error", message="Please enter a valid resource name and count.")
                return False
            calendar.resources[res_name]["count"] += inc
        
        calendar._save_resources("./templates/resources.json")
        return True