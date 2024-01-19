import lib
import gvars
import os
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from enum import Enum

class EnumCommand(Enum):
    """[Is used to Specify the type of Command will be used]\n
        CLICK = 1\n
        WRITE = 2\n
        GET_TEXT = 3\n
        CLEAR = 4\n
        GET_ELEMENT = 5\n
        GET_ELEMENTS = 6\n
        MOVE_TO = 7\n
        SELECT_OPTION = 8\n
    """
    CLICK = 1
    WRITE = 2
    GET_TEXT = 3
    CLEAR = 4
    GET_ELEMENT = 5
    GET_ELEMENTS = 6
    MOVE_TO = 7
    SELECT_OPTION = 8
    ACTION_CHAIN = 9
    RIGHT_CLICK = 10
    ENTER = 11

class EnumWindowHandler(Enum):
    """[Is used to Specify the type of Command will be used]\n
        NAVIGATE = 1\n
        NAVIGATE_BACK = 2\n
        NAVIGATE_FORWARD = 3\n
        REFRESH = 4\n
        SWITCH_TAB = 5\n
        QUIT = 6\n
    """
    NAVIGATE = 1
    NAVIGATE_BACK = 2
    NAVIGATE_FORWARD = 3
    REFRESH = 4
    SWITCH_TAB = 5
    QUIT = 6


def abrir_chrome(hide=False, cookie=False):
    
    """
    Função abrir_chrome:
    
    Entrada:
        
    Retornos: 
        driver                        # Sucesso ao abrir o chrome.
    """
    chrome = True
    while chrome:
        path_idchrome = gvars.path_idchrome
        session_id, ip_pag = False, False
        
        if os.path.isfile(path_idchrome):
            with open(path_idchrome, "r") as f:
                processados = f.read()
                try:
                    ip_pag, session_id = processados.replace('"', "").split(" ")
                except:
                    pass

        global driver

        lib.filelog(f"ip_pag: {ip_pag}")
        lib.filelog(f"session_id: {session_id}")

        if session_id:
            lib.filelog("attach_to_session")
            driver = attach_to_session(ip_pag, session_id)
            
            try:
                for handle in driver.window_handles:
                    driver.switch_to.window(handle)
                    break
        
                # maximize window
                driver.minimize_window()
                driver.maximize_window()

                return driver
            except: 
                path_idchrome = gvars.path_idchrome
                with open(path_idchrome, "w") as f:
                    json.dump("", f)
        else:
            chrome_options = Options()
            
            path_chromedriver = gvars.path_chromedriver_exe

            arguments = [
                '--lang=pt-BR', 
                '--start-maximized',
                '--disable-notifications',
                '--disable-logging',
                '--disable-gpu',
                '--no-sandbox',
                '--log-level=3'
            ]

            for argument in arguments:
                chrome_options.add_argument(argument)

            scriptDirectory = gvars.path_project_folder

            if cookie:
                chrome_options.add_argument(f"user-data-dir={scriptDirectory}\\userdata")

            if hide:
                chrome_options.add_argument('--headless')

            prefs = {"credentials_enable_service": False,
                    "profile.password_manager_enabled": False}

            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            extension_folder_path = gvars.path_chromedriver_folder + r'\resources\load_extensions'
            if not os.path.isdir(extension_folder_path):
                os.makedirs(extension_folder_path)

            extensions = os.listdir(extension_folder_path)     

            for file in extensions:
                chrome_options.add_extension(extension_folder_path + '\\' + file)

            # =====================================
            
            driver = webdriver.Chrome(executable_path=path_chromedriver, options=chrome_options)
            
            url = driver.command_executor._url
            session_id = driver.session_id
            
            endereco = str(url) + " " + str(session_id)
            chrome = False
            
            with open(path_idchrome, "w") as f:
                json.dump(endereco, f)

            return driver


def attach_to_session(executor_url, session_id):
    try:
        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        driver.close()
        driver.session_id = session_id
        driver.implicitly_wait(0) # seconds
        return driver
    except:
        pass


def wait_execute_script(*, driver, script, timeout = 30):
    """
    Entradas:
        driver (obj) : Instância do chrome
        script (str) : script a ser executado
        timeout (int) : tentar executar por quanto tempo?
    """
    
    # se o script nao tiver retorno, 
    if script[:6] != "return":
        # lib.filelog(f"Script não tinha 'return', adicionando!")
        script = f"return {script}"
        
    # salva a hora que começou o loop
    time_begin = int(round(time.time() * 1000))
    while True: #loop infinito
        time_now = int(round(time.time() * 1000))
        if (time_now - time_begin) / 1000 >= timeout:
            lib.filelog(f"timeout executando script após {(time_now - time_begin)/1000} segundos")
            return -1
            
        try:
            r = driver.execute_script(script)
            r = 1 if r is None else r
            return r
        except:
            time.sleep(1)


def wait_ready_state(*, driver, timeout = 60) :
    '''
    Descrição:
        Função para verificar o Ready State da página
    Inputs:
        driver (obj)          : Objeto do ChromeDriver
        timeout (int)         : Segundos para timeOut
    Outputs:
         1 (int) : Retorno bem sucedido
        -1 (int) : Erro
    '''
    ind_timeout = 0
    element_founded = False
    ready_state = ""
    
    while ind_timeout <= timeout and element_founded != True:
        try:
            ready_state = driver.execute_script("return document.readyState")
            if ready_state == "complete" :
                element_founded = True
        except:
            time.sleep(1)
            ind_timeout += 1

    if ind_timeout > timeout :
        lib.filelog("timeout ao esperar carregamento do browser")
        return -1

    return 1


def action(driver, command : EnumCommand, xpath, text='', wait_until=5, wait_before_find_sec=0, wait_after_find_sec=0, wait_after_interaction_sec=0):
    """
        Method of actions for selenium interaction, it needs the import of EnumCommand enum

        Parameters:\n
            command (EnumCommand): The action selenium will perform
            xpath (string): Location of the Element
            text (string): Content that will be written
            wait_until (int): Wait in sec For element to show, default: 20
            wait_before_find_sec (int): Wait before element is shown, default: 0
            wait_after_find_sec (int): Wait after the element is shown, default: 0
            wait_after_interaction (int): Wait after the interaction with the element, default: 0
    """
    wait = WebDriverWait(driver, wait_until)
    time.sleep(wait_before_find_sec)

    if command != EnumCommand.GET_ELEMENTS and command != EnumCommand.ACTION_CHAIN:
        element = WebDriverWait(driver, wait_until).until(EC.presence_of_element_located((By.XPATH, xpath)))
        time.sleep(wait_after_find_sec)

    if command is EnumCommand.CLICK:
        element.click()
    elif command is EnumCommand.WRITE:
        element.send_keys(text)
    elif command is EnumCommand.GET_TEXT:
        if element.text:
            return element.text
        else:
            return element.get_attribute('value')
    elif command is EnumCommand.CLEAR:
        element.clear()
    elif command is EnumCommand.GET_ELEMENT:
        return element
    elif command is EnumCommand.GET_ELEMENTS:
        return driver.find_elements(By.XPATH, xpath)
    elif command is EnumCommand.MOVE_TO:
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
    elif command is EnumCommand.SELECT_OPTION:
        Select(element).select_by_value(text)
    elif command is EnumCommand.ACTION_CHAIN:
        actions = ActionChains(driver)
        actions.send_keys(text).perform()
    elif command is EnumCommand.RIGHT_CLICK:
        action = ActionChains(driver)
        action.context_click(element).perform()
    elif command is EnumCommand.ENTER:
        actions = ActionChains(driver)
        actions.send_keys(Keys.ENTER).perform()

    time.sleep(wait_after_interaction_sec)


def window_action(*, driver, command: EnumWindowHandler, url = ''):
    """
        Method of actions for window manipulation, it needs the import of EnumWindowHandler enum

        Parameters:\n
            command (EnumWindowHandler): The action window will perform\n
            url (string): Only if you will go to another url\n
    """
    if command is EnumWindowHandler.NAVIGATE:
        driver.get(url)
    elif command is EnumWindowHandler.NAVIGATE_BACK:
        driver.back()
    elif command is EnumWindowHandler.NAVIGATE_FORWARD:
        driver.forward()
    elif command is EnumWindowHandler.REFRESH:
        driver.refresh()
    elif command is EnumWindowHandler.QUIT:
        time.sleep(2)
        driver.quit()

