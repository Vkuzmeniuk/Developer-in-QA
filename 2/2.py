import argparse

parser = argparse.ArgumentParser(description='Folder for synchronize')
parser.add_argument('origin', type=str, help='Origin folder')
parser.add_argument('replication', type=str, help='Replication folder')

parser.add_argument('--sync_time',type=int,default=600,help='Provide a time for sync (in second) (default: 600)')
parser.add_argument('--logs',type=str,default=".\\",help='Provide a folder for logs')
args = parser.parse_args()

import os, datetime, stat, copy, shutil, logging, schedule,time

dict_tmp={}

# def time_format(mtime):
#     return time.strftime("%D, Time: %H:%M:%S", time.gmtime(mtime))

def get_info_folder_files(fpath,dirpath,fnames):
    for fname in fnames:
        path=os.path.join(dirpath, fname)
        try:
            inf = os.stat(fname)
        except:
            return None
        dict_tmp[path]= (fpath,dirpath,fname,inf.st_mtime,inf.st_size)         
                    
def recursion_search(fpath):
    if os.path.exists(fpath):
        os.chdir(fpath)
        for dirpath, dirnames, filenames in os.walk("."):
            os.chdir(dirpath)
            get_info_folder_files(fpath,dirpath,dirnames)
            get_info_folder_files(fpath,dirpath,filenames)

def delete_elements(or_dict,rp_dict):
    dict_tmp=copy.deepcopy(rp_dict)
    for i in or_dict:
        try:
            dict_tmp.pop(i)
        except:
            continue
    
    for i in dict_tmp:
        path=os.path.normpath(os.path.join(rp_dict[i][0], i))
        if os.path.isfile(path):
            os.remove(path)
            log_tmp = f"{datetime.datetime.now()} - File \"{path}\" removed."
            logging.info(log_tmp)
            print(log_tmp)
        else:
            shutil.rmtree(path)
            log_tmp=f"{datetime.datetime.now()} - Folder \"{path}\" removed."
            logging.info(log_tmp)
            print(log_tmp)

def replace_elements(or_dict,rp_dict):
    for i in or_dict:
        try:
            if (or_dict[i][3]>rp_dict[i][3])or(or_dict[i][4]!=rp_dict[i][4]):
                or_path = os.path.normpath(os.path.join(or_dict[i][0], i))
                rp_path = os.path.normpath(os.path.join(rp_dict[i][0], i))
                shutil.copy(or_path, rp_path)
                log_tmp = f"{datetime.datetime.now()} - File \"{rp_path}\" replaced."
                logging.info(log_tmp)
                print(log_tmp)
        except:
            continue
    
def copy_elements(or_dict,rp_dict,fpath):
    dict_tmp=copy.deepcopy(or_dict)
    for i in rp_dict:
        try:
            dict_tmp.pop(i)
        except:
            continue
    for i in dict_tmp:
        or_path = os.path.normpath(os.path.join(dict_tmp[i][0], i))
        rp_path = os.path.normpath(os.path.join(fpath,dict_tmp[i][1]))
        if os.path.isfile(or_path):
            shutil.copy(or_path, rp_path)
            log_tmp = f"{datetime.datetime.now()} - File \"{dict_tmp[i][2]}\" copied to {rp_path}."
            logging.info(log_tmp)
            print(log_tmp)
        elif os.path.isdir(or_path):
            dir_path = os.path.normpath(os.path.join(rp_path, dict_tmp[i][2]))
            shutil.copytree(or_path, dir_path)
            log_tmp = f"{datetime.datetime.now()} - Folder \"{dict_tmp[i][2]}\" copied to {rp_path}."
            logging.info(log_tmp)
            print(log_tmp)

# orgn="D:\\GitHub\\Developer in QA\\Origin"
# rplct="D:\\GitHub\\Developer in QA\\Replicate"
# lgs="D:\\GitHub\\Developer in QA\\Logs"            
    
def sync():
    if os.path.exists(args.logs):
        os.chdir(args.logs)
    logging.basicConfig(filename="Logging.log", level=logging.INFO)
    
    dict_orgn={}
    dict_rplct={}
    
    recursion_search(args.origin)
    dict_orgn=copy.deepcopy(dict_tmp)
    dict_tmp.clear()
    
    recursion_search(args.replication)
    dict_rplct=copy.deepcopy(dict_tmp)
    dict_tmp.clear()
    
    delete_elements(dict_orgn,dict_rplct)
    
    recursion_search(args.replication)
    dict_rplct=copy.deepcopy(dict_tmp)
    dict_tmp.clear()
    
    copy_elements(dict_orgn,dict_rplct,args.replication)
    
    recursion_search(args.replication)
    dict_rplct=copy.deepcopy(dict_tmp)
    dict_tmp.clear()
    
    replace_elements(dict_orgn,dict_rplct)
    
schedule.every(args.sync_time).seconds.do(sync)
while 1:
    schedule.run_pending()
    time.sleep(1)
Timer(args.sync_time, sync).start()
