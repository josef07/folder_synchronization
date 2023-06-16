import os 
from datetime import datetime
import pathlib


SOURCE = pathlib.Path(input("Specify SOURCE directory: ")) #pathlib.Path is used to format path accordingly to operating system  
REPLICA = pathlib.Path(input("Specify REPLICA directory: "))
LOG = pathlib.Path(input("Specify LOG file: "))
INTERVAL = int(input("Please select interval in following format (e.g. 0 = constant check, 60 = 1 minute, 180 = 3 minutes etc..) "))

def check_path(source, replica, log):
    if (os.path.exists(source)) != True:
        ("You have entered incorrect source path")
    if (os.path.exists(replica)) != True:
        ("You have entered incorrect replica path")
    if (os.path.exists(log)) != True:
        ("You have entered incorrect log path")

def get_source_files(): 
    dict_s = {}
    with os.scandir(SOURCE) as source: 
        for entry in source: 
            name_and_time = [entry.name, entry.stat().st_mtime] #list of names and timestamps of last modification of a files 
            dict_s[entry.path] = name_and_time # keys of dictionary are full paths names of files in source file, values are names and timestamps of last modification 
    return dict_s

def get_replica_files():
    dict_r = {}
    with os.scandir(REPLICA) as replica:
        for entry in replica:
            name_and_time = [entry.name, entry.stat().st_mtime]
            dict_r[entry.path] = name_and_time
    return dict_r

def copy_files(source_path, replica_path):# copies file using command line
    os.system(f"copy {source_path} {replica_path}")

def remove_files(path_of_file): #removes file from folder
    os.remove(path_of_file)

def get_key(val, dict): #gets key from directory based on actual value
    for key, value in dict.items():
        if val == value:
            return key

def append_to_log(path, message): #writes log massage 
    with open(path, 'a') as k:
        k.writelines(message)

def compare_files():
    dict_s = get_source_files()
    dict_r = get_replica_files()
    if dict_s.values() != dict_r.values():
        for file in dict_r.values():
            if file not in dict_s.values(): #check if no additional files are present in replica folder, if there is additional file, remove 
                remove_files(get_key(file, dict_r))
                message = str(datetime.now()) + ' Removing unexpected file from replica folder ' + file[0]
                print(message)
                append_to_log(LOG, message + '\n')

        for file in dict_s.values(): #iterating over files in source folder 
            if file not in dict_r.values(): #compare if files in source folder are present in replica folder, if not, copy files to replica folder 
                copy_files(get_key(file, dict_s), REPLICA) 
                message = str(datetime.now()) + ' Copying actual file ' + file[0] +' to replica folder' 
                print(message) 
                append_to_log(LOG, message + '\n')
    else:
        print("source and replica folders are synchronized")


def main():
    check_path(SOURCE,REPLICA,LOG) #checks validity of entered paths 
    start = os.popen("time /t").read() #read time from command line and store it in variable, format HH:SS
    start_hours_in_sec = int(start[0:2])*3600 #converts hours to seconds
    start_minutes_in_sec = int(start[3:5])*60 #converts minutes to seconds 
    
    while(True): 
        try:
            now = os.popen("time /t").read()
            now_hours_in_sec = int(now[0:2])*3600
            now_minutes_in_sec = int(now[3:5])*60          
            if ((now_hours_in_sec+now_minutes_in_sec)-(start_hours_in_sec+start_minutes_in_sec)) >= INTERVAL: #specify interval values in seconds based on comand line values
                compare_files()

        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
