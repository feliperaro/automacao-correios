"""Chromedriver library"""

import time
import gvars

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def open_chrome(hide=False, cookie=False):
    """return chromedriver instance"""

    chrome_options = Options()

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

    script_directory = gvars.path_project_folder

    if cookie:
        chrome_options.add_argument(f"user-data-dir={script_directory}\\userdata")

    if hide:
        chrome_options.add_argument('--headless')

    chrome_options.add_experimental_option('excludeSwitches', [
        'enable-automation', 'enable-logging'
    ])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def wait_execute_script(*, driver, script, timeout = 30):
    """
    Entradas:
        driver (obj) : Instância do chrome
        script (str) : script a ser executado
        timeout (int) : tentar executar por quanto tempo?
    """

    if script[:6] != "return":
        script = f"return {script}"

    time_begin = int(round(time.time() * 1000))
    while True:
        time_now = int(round(time.time() * 1000))
        if (time_now - time_begin) / 1000 >= timeout:
            return -1
        try:
            r = driver.execute_script(script)
            r = 1 if r is None else r
            return r
        except Exception:
            time.sleep(1)
