import json
from modules.gvar import *
from modules.utils import *
import datetime
SAVE_ROOT = "./saved"

class BasicHandler:
    """
    this class is a base of IO in files
    """
    def __init__(self, res_path="./templates/resources.json"):     
        self.resources = {}
        self.chunk_size = 65535
        self.res_path = res_path

    def _load_json(self,filename):
        filename = os.path.realpath(filename)
        if self._ex_ext(filename) != 'json':
            raise Exception("need a json file")
        with open(filename,'r') as tmp:
            data = self._jsonstr_to_dict(tmp.read(2**30))
            tmp.close()
            
        return data


    def _load_resources(self,filename):
        filename = os.path.realpath(filename)
        data = self._load_json(filename)
        self.resources = data


    def _save_resources(self,filename = None):
        if filename == None:
            filename = self.res_path
        filename = os.path.realpath(filename)
        data = self._dict_to_jsonstr(self.resources)
        tmp = open(filename,'w')
        tmp.write(data)
        tmp.close()


    def _ex_ext(self,filename):
        filename = os.path.realpath(filename) # extract extension function
        filename = filename.split('.')
        return filename[-1] # this works (read in docs.python.org)


    def _jsonstr_to_dict(self,json_data) -> dict:
        return json.loads(json_data)


    def _dict_to_jsonstr(self,dict_data):
        return json.dumps(dict_data,indent=3)


    def _load_tasks(self,name):
        filename = os.path.realpath(name)
        data = self._load_json(name)
        self.available_tasks = data
