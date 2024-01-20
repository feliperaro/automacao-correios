"""Global variables"""
import os

ENV = "prd"
URL_CORREIOS = "https://www.sitecorreios.com.br/"

path_project_folder = os.getcwd()
path_chromedriver_folder = f"{path_project_folder}\\chromedriver"
path_chromedriver_exe = f"{path_chromedriver_folder}\\chromedriver.exe"
path_idchrome = f"{path_chromedriver_folder}\\idchrome.json"
path_downloads = f"{path_chromedriver_folder}\\resources\\downloads"
