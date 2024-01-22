from datetime import date
from datetime import datetime
import codecs
import os
import gvars

log_config = {
    'folder' : gvars.path_log, 
    'process_name' : gvars.PROCESS_NAME,
}


def filelog(append_message=None, hard_disable_print=False, config_log=log_config):
    """FILELOG"""
    
    log_folder = config_log['folder']
    try:
        os.mkdir(log_folder)
    except:
        pass
    
    process_name = config_log['process_name']
    log_process_name = f"log_{process_name}"
    
    process_log_path = os.path.join(log_folder, log_process_name)
    try:
        os.mkdir(process_log_path)
    except:
        pass
    
    today_date = date.today()
    today_date = str(today_date)
    
    filename = f'{today_date}-log.txt'
    log_file = f"{process_log_path}/{filename}"
    
    try:
        file_path = open(log_file, 'r+')
        file_path.close()
    except FileNotFoundError:
        file_path = open(log_file, 'w+')
        file_path.close()
        
    append_message = '<Blank Message>' if append_message is None else append_message
    time_now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    full_string = str(time_now) + ' - ' + str(append_message) + "\n"

    if not hard_disable_print:
        print(full_string)

    try:
        with codecs.open(log_file, 'a+', 'utf-8-sig') as out_file:
            out_file.writelines(full_string)
    except UnicodeEncodeError:
        full_string = full_string.encode('ascii', errors='ignore').decode('ascii')
        with codecs.open(log_file, 'a+', 'utf-8-sig') as out_file:
            out_file.writelines(full_string)
    except Exception as error:
        print(f"Erro ao gravar FileLog().\nfile: '{log_file}'.\nmensagem: '{append_message}'.\nerror: '{error}'.")

