from modules.iohandler import *

class event(BasicHandler):
    next = None
    start = 0
    end = 0
    notes = ""
    def __init__(self,_json:dict):
        """
        this constructor requires a json with
        resources: list of resources
        date-range: a list with two dates in isoformat
        time-range: same date but in minutes
        name: the name of task
        note: a note for this task
        """
        try:
            self.need_resources:list = _json["resources"]
            self.date                = _json["date-range"]
            self.time:list           = _json['time-range']  # minute when it starts
            self.task:str            = _json['name']     
            self.start               = int(self.time[0])
            self.end                 = int(self.time[1])
            if "notes" in _json.keys():
                self.notes           = _json["notes"]
            
            if self.start > self.end:
                raise Exception("Invalid range [R < L]")
            
            self._load_resources("./templates/resources.json")
            deps = set()
            for x in self.need_resources:
                deps.add(x)
           
            for resource in self.need_resources:
                needed = get_sources_dependency(self.resources, resource)
                for required in needed:
                    deps.add(required)
           
            no_use = set()
            for resource in deps:
                for el in self.resources[resource]["without"]:
                    no_use.add(el)
           
            collisions = deps & no_use
            if len(collisions) > 0:
                raise BaseException("invalid task, collision detected")
            self.need_resources = list(deps)

        except Exception as e:
            log(f"error initializing event [{e}]")

    def __str__(self):
        return json.dumps(self.__dict__())

    def __dict__(self):
        return {
            "time-range": self.time,
            "date-range": self.date,
            "resources" : self.need_resources,
            "name":self.task,
            "notes": self.notes
        }
    
    def get_no_utilization(self,res:str):
        """
        this function returns a list of resources that
        the param does not require to work
        """
        excluded = []
        for x in self.resources[res]["without"]:
            excluded.append(x)
        return excluded
