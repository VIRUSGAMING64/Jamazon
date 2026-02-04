from threading import Thread
from customtkinter import *
from CTkMessagebox import CTkMessagebox as Messagebox
import time
from modules.utils import *
from modules.gvar import calendar
class TaskRemover(CTkToplevel):
    selected = None

    def __init__(self):
        super().__init__()
        self.after(100, self.lift)
        self.x_size = 400
        self.y_size = 400

        self.title("Task Remover")
        self.geometry(f"{self.x_size}x{self.y_size}")
        self.resizable(False,False)
        
        self.eventos = CTkComboBox(self,200,command=self.update_label)
        self.eventos.pack()
        self.eventos.place()
        
        self.remove_button = CTkButton(self, text="Remove this event", command=self.remove)
        self.remove_button.pack()
        self.remove_button.place(
            x = (self.x_size - self.remove_button._current_width)//2,
            y = self.y_size - self.remove_button._current_height
        )
        
        self.info = CTkLabel(self,text="Information")
        self.info.pack()
        self.info.place(y = 28 , x = 0)


        self.update_thread = Thread(target = self.update_combo, daemon = True)
        self.close = False
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    

    def on_closing(self):
        self.close = True
        self.destroy()


    def run_updater(self):        
        self.update_thread.start()


    def update_combo(self):
            while True:
                if self.close:
                    break
                time.sleep(1)
                print("updating remover")
                labels = build_event_option_labels(calendar.events)
                try:
                    self.eventos.configure(values = labels)
                except Exception as e:
                    log(f"error in update_combo [{e}]")


    def remove(self):
        if self.selected == None:
            Messagebox(
                self, 300, 300,"ERROR", "[ERROR] Select one event"
            )
            return
        
        calendar.remove(self.selected)
        calendar.save_json_data()
        sl = self.selected
        self.selected = None
        self.info.configure(text = "")
        Messagebox(self,300,300,"REMOVED", F"TASK [{sl}] REMOVED")
        

    def update_label(self,selected):
        idx = parse_event_option(selected)
        if idx is None or idx >= len(calendar.events):
            self.selected = None
            return
        self.selected = idx
        ev = calendar.events[idx]
        self.info.configure(text = format_event_info(ev))