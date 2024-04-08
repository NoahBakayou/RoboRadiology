import json 
import os
from time import sleep
import random as r 
class File():
    def __init__(self, file):
        print('file localization...')
        self.file = file
        self.content_list = None
        self.content_length = None
        self.print = 0
    def check_file(self, file) -> bool:
        try: 
            os.stat(file).st_size == 0
            return True
        except:
            return False
    def create_list(self):
        if self.print:
            print("Converting task file to list...")
 
        with open(self.file, "r") as f:
            content = f.read()
            self.content_list = content.split('\n')
 
        self.content_length = len(self.content_list)
 
        if self.print:
            print(f'List created with {self.content_length} items.')
 
    def print_contents(self):
        count = 0
        if self.content_list:
            for task in self.content_list:
                print(f"{count} -> {task}")
                count +=1
        else:
            print("Empty list.")
 
#TODO: Create barcode application with this.
            #-> Using this for prototype 
                        # migrate to SQL eventually
#TODO: Creating src / test directories if they dont exist
class JSON_Database(File):
    #TODO: Print statements...
    def __init__(self, json_name):
        print('starting db....')
        if json_name.endswith('.json'):
            self.json_name = json_name[0:-5]
            self.json_file = json_name
        else:
            self.json_name = json_name
            self.json_file = json_name + '.json'
 
        super().__init__(self.json_file)
        self.class_list = []
        self.json_length = None
        self.json_data = None
        self.class_name = None
        self.pause_status = 0
        self.print = 0
 
        self.setup()
 
    #TODO: Get classes...
 
    def setup(self):
        print('setup....')
        self.pause()
        self.create_json()
 
 
    #TODO: not using this function yet, want to make it 
    # a little more polished though it might not need that for this.. 
            # -> switch cases  ? 
 
    # changing the name to make it clear that this 
                # - > function read and writes  
 
 
    # only use when updatinh json (not changing i t...)
    def write(self, json_dump):
        with open(self.json_file, 'w') as json_file:
            json.dump(json_dump, json_file, indent = 4)
 
    def json_add(self, data):
        print(f'Adding to {self.json_file}')
        #self.load_data()
        json_data = self.json_data 
        json_data[self.class_name].append(data)
        #TODO: If more than one class name, choose which one to add 2
        if self.print:
            print(json_data[self.class_name]) 
 
        with open(self.json_file, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
 
        print("Added to json.")
 
    #TODO: Look into having a write function to declutter with open statements.
        #TODO: lowk redundant.... for wat lol..... u can see what u do with each 
                # statement so it makes sense ?  
    # TODO: reload data after updating ?  
            #-> Figure out why it doesnt update with load_data after I add 
                    #  ->  to a class...
    def reload(self):
        return
 
    def add_class(self, class_name):
        if(class_name in self.class_list):
            print('class already exists...')
            return
        else:
            data = {class_name : []}
            try:
                with open(self.json_file, 'w') as json_file:
                    json.dump(data , json_file, indent=4)
                self.class_list.append(class_name)
                # reload data 
                self.reload_data()
            except:
                print("?????")
 
    #TODO: menu that displays classes to add from ? 
        #TODO: data should be similar formats within each class:
                # - >  should be implemented in the main file.
    def reload_data(self):
        print('reloading data...')
        with open(self.json_file, 'r') as json_file:
            data = json.load(json_file)
 
 
        self.json_data = data
 
        print(self.json_data)
 
 
    def add_data(self, class_name, data):
        if class_name in self.class_list:
            #TODO: Optimize memory issue by switching data base or 
                    # - > calling when necessary 
                        #-> might be more efficient to 
                                # load data by class once already created.
 
            # reload self.json_data
            self.reload_data() 
            print(self.json_data)
            self.json_data[class_name].append(data)
 
            self.write(self.json_data)
            #yap  
                # at the end bc we update self.json_data 
                #TODO: might cause issues; doing this to help with 
                        #performance  ? memory ?  idk 
                        # i can already feel the bugs with this though
                        #TODO: if i update self.json_data anyways dont need it
        #                self.load_data()
 
 
 
 
        else:
            print('class does NOT exist....')
 
 
    def pause(self):
        if self.pause_status:
            print('.')
            sleep(1)
        return
 
    def create_json(self):
        print(f'checking if {self.json_file} exists...')
        self.pause()
        if os.path.exists(self.json_file):
            if self.print:
                print(f"{self.json_file} exists asf :)") 
                print(f"Loading data from {self.json_file}...")
                self.pause()        
 
            self.load_data()
        else:
            if self.print:
                print(f"{self.json_file} does not exist asf :(")
                print("Creating file...")
                self.pause()
 
            # create file 
            empty_json = {}
            with open(self.json_file, 'w') as json_file:
                json.dump(empty_json, json_file, indent = 4)
            self.create_json()
 
 
 
    def load_data(self):
        if self.check_file(self.json_file):
            with open(self.json_file, 'r') as json_file:
                data = json.load(json_file)
            # TODO: load json object names ... 
            self.json_data = data
            for key, value in enumerate(data):
                self.class_list.append(value)
            if self.print and 0:
                print(f'data inside da json ->\n\n{data}\n\ndata stored inside self...\n\n{self.json_data}\n\n')
        else:
            print('empty? ')
 
    def print_data(self):
        print(self.json_data)