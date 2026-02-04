from modules.events import *
from modules.SegTree import *


class Calendar(BasicHandler):
    
    def __init__(self,used_res = "used_resources.json", actives_ev = "actives_events.json"):
        try:
            super().__init__()
            self._load_resources("./templates/resources.json")
            self.used_resources:dict        = {}
            self.available_tasks:dict       = {}
            self.events:list[event]         = []
            self.inqueue:dict[event,bool]   = {} 
            self.actives_events_path        = actives_ev
            self.used_res_path              = used_res
            self.load_used_resources(f"{SAVE_ROOT}/{used_res}")
            ex                              = self._load_json(f"{SAVE_ROOT}/{actives_ev}")
            self.events                     = []
            for i in ex:
                self.events.append(event(i))
            self.save_json_data()

        except Exception as e:
            log(f"error loading used resources: ",e)


    def _save_tasks(self,filename = None):
        if filename == None:
            filename = "./templates/tasks.json"
        filename = os.path.realpath(filename)
        data = self._dict_to_jsonstr(self.available_tasks)
        tmp = open(filename,'w')
        tmp.write(data)
        tmp.close()

    def list_events(self): 
        return self.events

    def load_used_resources(self, filename):
        self.used_resources = self._load_json(filename)


    def save_json_data(self) -> None:
        sv:list = []
        for ev in self.events:
            sv.append(ev.__dict__())
            
        os.makedirs(SAVE_ROOT, exist_ok=True)
        fi = open(f"{SAVE_ROOT}/{self.actives_events_path}","w")
        fi.write(json.dumps(sv,indent=3))
        fi.close()
        try:
            save_used_resources = self._dict_to_jsonstr(self.used_resources)
            fi = open(f'{SAVE_ROOT}/{self.used_res_path}',"w")
            fi.write(save_used_resources)
            fi.close()
        except Exception as e:
            print("maybe you don't have access to this file: ",e)



    def gen_tree(self, res , l , length):    
        id = 0
        a2 = [l,l + length, l+1,l + length+1]
        di = {}
        for i in self.events:
            if not res in i.need_resources:
                continue
            a2.append(i.end)
            a2.append(i.start)
            a2.append(i.start+1)
            a2.append(i.end + 1)
    
        a2.sort()
        for x in a2:
            if di.get(x,-1) == -1:
                di[x] = id
                id += 1
        tree = SegTree([0] * (id + 10) )
        
        for x in self.events:
            if not res in x.need_resources:
                continue
            start_idx = di[x.start]
            end_idx = di[x.end]
            tree.update(start_idx, end_idx, 1)
        return di,tree



    def check_available(self, new_res: str, start: int, end: int, di , tree):
        if not (new_res in self.used_resources.keys()):
            return True, None
        try:
            if start not in di or end not in di:
                log(f"check_available: keys not found - start={start} in di: {start in di}, end={end} in di: {end in di}")
                return True , None
            l = di[start]
            r = di[end]
            mx = tree.query(l,r)
            if mx >= self.resources[new_res]["count"]:
                return False,new_res
        except Exception as e:
            log("error checking available resource: ", str(e))
            return False,None
        return True,None



    def add_event(self,new:event,check = True):
        self.sort()
        try:
            if check == True:
                for res in new.need_resources:
                    di,tree = self.gen_tree(res,new.start,new.end - new.start)
                    av, t_res = self.check_available(res, new.start, new.end, di, tree)
                    if av == False:
                        return av,t_res
            
            self.events.append(new)
            self.inqueue[new] = True

            for res in new.need_resources:     
                add_to_dict(self.used_resources,[res,new.start,1])        
                add_to_dict(self.used_resources,[res,new.end,-1])
        
            return True,None
        
        except Exception as e:
            log("error adding event: [unknown error]", e)
        return False,None



    def remove(self,index):
        deleted = self.events.pop(index)
        for res in deleted.need_resources:
            add_to_dict(self.used_resources,[res,deleted.start, -1])
            add_to_dict(self.used_resources,[res,deleted.end, 1])
        del self.inqueue[deleted]


    def remove_old_events(self):
        self.sort()
        init_t = tominute(datetime.datetime.now())
        events = []
        for task in self.events:
            if init_t < task.end:
                events.append(task)

        self.used_resources = {}
        self.events  = []

        for x in events:
            self.add_event(x,False)



    def sort(self):
        """
        this function sorts keys of self.used_resources by age
        """
        temp = {}
        for res in self.used_resources:
            temp[res] = {}
            keys = list(map(int,self.used_resources[res].keys()))
            keys.sort()
            for key in keys:
                temp[res][str(key)] = self.used_resources[res][str(key)]

            for key in keys:
                self.used_resources[res][str(key)] = temp[res][str(key)]
        self.used_resources = {}
        for res in temp:
            self.used_resources[res] = temp[res]



    def suggest_brute_lr(self, L: int, R: int, resources: list):
        length = (R-L)
        print(type(L),type(R))
        l = tominute(datetime.datetime.now())
        start = datetime.datetime.now()
        self.sort()        
        while True:
            av = True
            for res in resources:
                di, tree = self.gen_tree(res, l, length)
                av , t_res= self.check_available(res, l, l + length, di, tree)
                if not av:
                    av = False
                    mx: int = 10**300
                    for x in self.list_events():
                        if (l < x.end):
                            mx = min(mx, x.end + 1)

                    if mx == 10**300:
                        mx = l + 1
                        
                    ant: int = l
                    l: int = mx
                    print(mx,start.isoformat())
                    dif: int = l - ant
                    dr = datetime.timedelta(minutes=dif)
                    start += dr
                    break

            if av:
                return start