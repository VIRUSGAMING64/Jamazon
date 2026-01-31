from customtkinter import *
import datetime
from modules.utils import *
from modules.gvar import calendar
from modules.events import *
from CTkMessagebox import CTkMessagebox as Messagebox

class TaskCreator(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.after(100, self.lift)  # Ensures that the window appears in front on Windows
        self.title("TASK ADDER")
        self.x_size = 480
        self.y_size = 300
        self.geometry(f"{self.x_size}x{self.y_size}")
        
        """Time labels and text boxes."""
        self.begin_time_label = CTkLabel(self, text="Begin time:")
        self.end_time_label = CTkLabel(self, text="End time:")
        
        self.begin_time = CTkTextbox(self, height=28, border_color="blue")
        self.end_time = CTkTextbox(self, height=28, border_color="blue")

        start_time = datetime.datetime.now().isoformat().rsplit(":", 1)[0]
        print(start_time)

        self.begin_time.pack(pady=20)
        self.end_time.pack(pady=20)

        self.begin_time_label.pack(pady=0)
        self.end_time_label.pack(pady=0)
        
        self.begin_time.place(x=self.x_size - 200 - 200, y=0)
        self.begin_time_label.place(x=self.x_size - 275- 200, y=0)

        self.begin_time.bind("<Return>", lambda event: "break")
        self.end_time.bind("<Return>", lambda event: "break")
        
        self.end_time.place(x=self.x_size - 200- 200, y=28)
        self.end_time_label.place(x=self.x_size - 265- 200, y=28)
        
        self.begin_time.insert("1.0", start_time.replace('T', ' AT '))
        self.end_time.insert("1.0", start_time.replace('T', ' AT '))

        """Show resources that this event needs."""
        self.tasks = CTkComboBox(
            self,
            width=280,
            values=self._get_tasks(),
            state="readonly",
            command=self._get_deps,
        )
        self.tasks.set("Select a task")
        self.tasks.pack()
        self.tasks.place(x=0, y=56)

        """Dependency label."""
        self.dependency_label = CTkLabel(self, text="Dependencies:\n")
        self.dependency_label.pack()
        self.dependency_label.place(x=0, y=90)

        """Buttons."""
        self.b_add = CTkButton(self, text="Add this event", command=self.add_event)
        self.b_add.pack()
        self.b_add.place(x=70, y=self.y_size - 30)


        self.adjust_button = CTkButton(self, text="Adjust date", command=self.adjust)
        self.adjust_button.pack()
        self.adjust_button.place(x=70, y=self.y_size - 60)

        """Notes textbox"""
        self.notes = CTkTextbox(self,height = self.y_size,width =200)
        self.notes.insert("1.0","Task notes")
        self.notes.pack()
        self.notes.place(x = 280, y = 0)


    def _get_deps(self, selected):
        deps = []
        print(selected, calendar.available_tasks)

        res = calendar.available_tasks[selected]["resources"]
        for t in res:
            deps.append(t["name"])
        
        A = set()
        for i in deps:
            A.add(i)
            for x in get_sources_dependency(calendar.resources, i):
                A.add(x)
        
        print(A)
        deps = []
        for i in A:
            deps.append(i)
        print(deps)
        org = self.dependency_label.cget("text").split(':')[0]
        ne = ""
        for i in deps:
            ne += f"- {i}\n"

        self.dependency_label.configure(text=org + ":\n" + ne)
        return deps

    def __suggest(self, l: int, r: int, resources: list) -> list:
        print("running...")
        L = calendar.suggest_brute_lr(l, r, resources)
        print("found...")
        R = L + datetime.timedelta(minutes=r - l)
        return L, R


    def adjust(self):
        print("[SUGGEST_FUNCTION]")
        begin = self.begin_time.get("1.0","19.0").replace(" AT ","T").replace("\n","")
        end = self.end_time.get("1.0","19.0").replace(" AT ","T").replace("\n","")
        valid =  CheckISODate(begin)
        valid *= CheckISODate(end)
        print("initializing suggestion...")
        if valid == 0:
            self.show_invalid("date")
            return False
        
        begin = datetime.datetime.fromisoformat(begin)
        end = datetime.datetime.fromisoformat(end)
        
        if begin >= end:
            self.show_invalid("[begin >= end]")
            return False
        
        selected_task = self.tasks.get()
        if (selected_task == "Select a task"):
            Messagebox(
                self,200,200,"Not selected",
                "Select one task"
            )
            return
        
        res = self._get_deps(selected_task)
        l,r = self.__suggest(tominute(begin), tominute(end), res)
        l   = str(l.isoformat().replace('T', ' AT ').split(".")[0])
        r   = str(r.isoformat().replace('T', ' AT ').split(".")[0])
        l   = l.rsplit(":",1)[0]
        r   = r.rsplit(":",1)[0]
        
        print(l)
        print(r)
        
        self.begin_time.delete("1.0","19.0")
        self.end_time.delete("1.0","19.0")
        
        self.begin_time.insert("1.0", l)
        self.end_time.insert("1.0", r)
        return True

    def _get_tasks(self) -> list:
        tasks = []
        for x in calendar.available_tasks:
            tasks.append(x)
        tasks.sort()
        return tasks

    def show_invalid(self, data):
        Messagebox(
            height=100,
            width=100,
            title="ERROR",
            message=f"Invalid {data}",
            option_1="Accept"
        )


    def _add_event(self):
        begin   = self.begin_time.get("1.0","19.0").replace(" AT ","T").replace("\n","")
        end     = self.end_time.get("1.0","19.0").replace(" AT ","T").replace("\n","")
        notes   = self.notes.get("1.0","end")
        valid   = CheckISODate(begin)
        valid  *= CheckISODate(end)
    
        if valid == 0:
            self.show_invalid("date")
            return False

        task_name = self.tasks.get()
        if (task_name == "Select a task"):
            Messagebox(
                self,200,200,"Not selected",
                "Select one task"
            )
            return
        
        res = self._get_deps(task_name)
        new = event(
            {
                "name": task_name,
                "time-range": [
                    tominute(datetime.datetime.fromisoformat(begin)),
                    tominute(datetime.datetime.fromisoformat(end))
                ],
                "resources": res,
                "date-range": [begin,end],
                "notes": notes
            }
        )
        
        if new.start >= new.end:
            message = Messagebox(
                height=100,
                width=100,
                title="ERROR",
                message="The end of the task is equal to the beginning!",
                option_1="Accept"
            )
            message.get()
            return False
        
        added = calendar.add_event(new)
        calendar.save_json_data()
        if added: Messagebox(self,200,200,"Added", "Task added successfully !")
        print(f"added: [{added}]")
        return added
    

    def add_event(self):
        message = Messagebox(
            height=100,
            width=100,
            title="Adding event",
            message="Add this event?",
            option_1="Accept",
            option_2="Cancel"
        )
        response = message.get()
        if response == "Cancel":
            print("User canceled the event addition.")
            return False
        elif response == "Accept":
            added = self._add_event()

        if not added:
            Messagebox(self,200,200,"Problem adding", message="Not added task")
            return False
    
        return added