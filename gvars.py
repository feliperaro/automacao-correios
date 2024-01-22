"""Global variables"""
import os

ENV = "prd"
PROCESS_NAME = "consulta_encomenda"
URL_CORREIOS = "https://www.sitecorreios.com.br/"

path_project_folder = os.getcwd()
path_chromedriver_folder = f"{path_project_folder}\\chromedriver"
path_chromedriver_exe = f"{path_chromedriver_folder}\\chromedriver.exe"
path_idchrome = f"{path_chromedriver_folder}\\idchrome.json"
path_downloads = f"{path_chromedriver_folder}\\resources\\downloads"
path_output = f"{path_project_folder}\\output"
path_log = f"{path_output}\\logs"
