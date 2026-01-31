print("MAIN POINT STARTED")
from modules import *

set_appearance_mode("dark")


class app(CTk):
    """
    This is a main window
    """

    def __init__(self):
        super().__init__()
        """construction all buttons"""

        self.pack_propagate(False)
        self.title("Jamazon - tasks administrator")
        self.task_creator = None
        self.task_remover = None
        self.size_x = 512
        self.size_y = 256
        self.geometry(f"{self.size_x}x{self.size_y}")

        self.ButtonTaskCreator = CTkButton(self,text="Create new task",command=self.create_task)
        self.ButtonTaskCreator.pack()
        self.ButtonTaskCreator.place(x=(self.size_x - self.ButtonTaskCreator._current_width)//2)

        self.ButtonTaskRemover = CTkButton(self,text="Remove existing task",command=self.remove_task)
        self.ButtonTaskRemover.pack()
        self.ButtonTaskRemover.place(
            x=(self.size_x - self.ButtonTaskRemover._current_width)//2,
            y=30
        )

        self.button_res_adder = CTkButton(self,text="Add Resource",command=self.open_res_adder)
        self.button_res_adder.pack()
        self.button_res_adder.place(
            x=(self.size_x - self.button_res_adder._current_width)//2,
            y=60
        )

        self.button_ev_shower = CTkButton(self,text="Show tasks",command=self.show)
        self.button_ev_shower.pack()
        self.button_ev_shower.place(
            x=(self.size_x - self.button_ev_shower._current_width)//2,
            y=90
        )

        
        self.button_ev_adder = CTkButton(self,text="New type of task",command=self.open_event_creator)
        self.button_ev_adder.pack()
        self.button_ev_adder.place(
            x=(self.size_x - self.button_ev_adder._current_width)//2,
            y=120
        )
        
        self.resource_show = CTkButton(self,text="Show all resources",command=self.show_resources)
        self.resource_show.pack()
        self.resource_show.place(
            x=(self.size_x - self.resource_show._current_width)//2,
            y=150
        )

        self.ev_shower       = None
        self.ev_creator      = None
        self.res_adder       = None
        self.resource_shower = None
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    

    def kill_window(self,wind):
        if wind is not None:
            try:
                wind.destroy()
                wind = None
            except Exception as e:
                log(f"kill window: [{e}]")
        else:
            log("window is None, can't kill it")

    def open_event_creator(self):
        self.kill_window(self.ev_creator)
        self.ev_creator = EventCreator()
        self.ev_creator.resizable(False,False)


    def open_res_adder(self):
        self.kill_window(self.res_adder)
        self.res_adder = RessAdder()
        self.res_adder.resizable(False,False)


    def remove_task(self):
        if self.task_remover is not None:
            self.task_remover.close = True
            
        self.kill_window(self.task_remover)
        self.task_remover = TaskRemover()
        #self.task_remover.resizable(False,False)
        self.task_remover.run_updater()

    def create_task(self):
        self.kill_window(self.task_creator)
        self.task_creator = TaskCreator()
        self.task_creator.resizable(False,False)

    def show_resources(self):
        self.kill_window(self.resource_shower)
        self.resource_shower = ResourceShower(calendar.resources)
        
    def show(self):
        self.kill_window(self.ev_shower)
        self.ev_shower = EventShower(calendar.events)

    def on_closing(self):
        self.kill_window(self.task_creator)
        self.kill_window(self.task_remover)
        self.kill_window(self.ev_creator)
        self.kill_window(self.res_adder)
        self.kill_window(self.ev_shower)
        self.kill_window(self.resource_shower)
        self.destroy()
        import sys
        sys.exit(0)



print("removing olds events")
calendar.remove_old_events()
APP = app()
APP.resizable(False,False)
APP.mainloop()