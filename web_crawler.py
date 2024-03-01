# -*- Coding: UTF-8 -*-
# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

"""
Ferramenta gerencia os processos no navegador
author: Teonas Gonçalves Dourado Netto
e-mail: teonasnetto@gmail.com
version: 1.0.0
date: 2022-02-09
"""

import os
import traceback
from datetime import datetime
from time import sleep
import shutil
import random
from dotenv import load_dotenv
import pyautogui

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
from PIL import Image

from directories import Directories
from access import Access
from files import Files
from gdrive import GDrive
from gsheets import Psheets

# diretorios
_dir = Directories()

# acessos
access = Access()

# Files
files = Files()

# Gsheets
gsheets = Psheets()

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class WebCrawler:  # pylint: disable=line-too-long
    """
    Funções para trabalhar diretamente no navegador
    """

    def start_chorme_driver(self, headless=False):  # type: ignore
        """
        Inicialização da configuração do selenium usando o chromedriver
        """
        print('#Fechando instancias antigas')
        proccess_name = os.getenv('CHROME_PROCCESS_NAME').strip('\\')
        os.system(f'wmic process where name="{proccess_name}" delete')
        print('#Acessando selenium no chrome')
        print('#Iniciando chormeDriver')
        chrome_options = Options()
        prefs = {"download.default_directory": _dir.dir_temp,
                 "download.prompt_for_download": False,
                 "download.directory_upgrade": True}
        chrome_options.add_experimental_option("prefs",
                                               prefs)
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('no-sandbox')
        chrome_options.add_argument('disable-gpu')
        chrome_options.add_argument('disable-dev-shm-usage')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
        # chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")
        # Romove os avisos e mantem somente os erros
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-logging")

        if os.getenv("CHROME_CACHE") is not None and os.getenv("CHROME_CACHE").startswith('C:'):
            chrome_cache = os.getenv("CHROME_CACHE")
        elif os.getenv("CHROME_CACHE") is not None and os.getenv("CHROME_CACHE").startswith('\\'):
            chrome_cache = os.path.join(_dir.dir_data, os.getenv("CHROME_CACHE").strip("\\"))

        if os.getenv("CHROME_BINARIES_PATH") is not None and os.getenv("CHROME_BINARIES_PATH").startswith('C:'):
            chrome_binaries = os.getenv("CHROME_BINARIES_PATH")
        elif os.getenv("CHROME_BINARIES_PATH") is not None and os.getenv("CHROME_BINARIES_PATH").startswith('\\'):
            chrome_binaries = os.path.join(_dir.dir_data, os.getenv("CHROME_BINARIES_PATH").strip("\\"), os.getenv("CHROME_PROCCESS_NAME").strip("\\"))

        if os.getenv("CHROMEDRIVER") is not None and os.getenv("CHROMEDRIVER").startswith('C:'):
            chromedriver = os.getenv("CHROMEDRIVER")
        elif os.getenv("CHROMEDRIVER") is not None and os.getenv("CHROMEDRIVER").startswith('\\'):
            chromedriver = os.path.join(_dir.dir_data, os.getenv("CHROMEDRIVER").strip("\\"))

        if not os.path.isfile(chromedriver) or not os.path.isfile(chrome_binaries):
            print("Chromedriver/Chromium não encontrado. Baixando...")
            try:
                shutil.rmtree(os.path.join(_dir.dir_data, os.getenv('CHROME_BINARIES_PATH').strip('\\')))
            except:
                pass
            gdrive = GDrive(_dir.dir_data, 'service_account')
            gdrive_content = gdrive._list_folder_content(os.getenv("GDRIVE_CHROME_ID"))
            df_gdrive_BD = pd.DataFrame.from_dict(list(gdrive_content.items()))
            file_id = df_gdrive_BD.loc[df_gdrive_BD[0] == os.getenv('ZIP_CHROME_NAME'), [1]].values[0][0]
            file_name = df_gdrive_BD.loc[df_gdrive_BD[0] == os.getenv('ZIP_CHROME_NAME'), [0]].values[0][0]
            gdrive._download_file(file_id, os.path.join(_dir.dir_temp, file_name))
            files.unzip_files(os.path.join(_dir.dir_data, file_name.split('.')[0]))
            os.rename(os.path.join(_dir.dir_data, os.getenv('CHROME_BINARIES_PATH').strip('\\'), 'chromiumportable.exe'), os.path.join(_dir.dir_data, chrome_binaries))
            os.remove(os.path.join(_dir.dir_temp, file_name))

        chrome_options.add_argument('user-data-dir=' + chrome_cache)
        chrome_options.binary_location = chrome_binaries
        global driver
        try:
            driver = webdriver.Chrome(service=Service(chromedriver), options=chrome_options)
            stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )
        except Exception as _e:
            traceback.print_exc()
            print(_e)

    def quit_chrome_driver(self) -> None:
        """
        Fechar o chromedriver
        """
        print('#Fechando navegador')
        driver.quit()

    def log_into_gpm(self, operation: str) -> None:
        """
        Realizar login no GPM
        """
        try:
            print('#Logando portal GPM-BA')
            driver.get(f"https://sirtec{operation}.gpm.srv.br/")

            try:
                driver.find_element(By.PARTIAL_LINK_TEXT, "Sair")

            except:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "form_login")))
                driver.find_element(
                    By.ID, "idLogin").send_keys(access.login_gpm)
                driver.find_element(
                    By.ID, "idSenha").send_keys(access.passw_gpm)
                driver.find_element(By.XPATH, "//input[5]").click()
        except Exception as _e:
            print(_e)
            driver.quit()

    def consulta_servicos_gpm(self):
        """
        Abre o consulta serviços do GPM para baixar o relatório das notas que foram repassadas pelo clipboard no clipboard_IW59_GPM().
        """
        try:
            print('#Abrindo consulta serviços')
            driver.get("https://sirtecba.gpm.srv.br/gpm/geral/consulta_servico.php")

            # Adiciona o status aberto na situação do serviço
            situacao = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/form[4]/table/tbody/tr[11]/td[2]/div/input")))
            situacao.send_keys('Aberto')
            sleep(.5)
            situacao.send_keys(Keys.RETURN)

            wks = gsheets.worksheet_select('bd_config_SESMT', 'servicos_download_gpm')
            df_servicos_download_gpm = wks.get_as_df()

            tipos_servicos = df_servicos_download_gpm['TIPO SERVICO'].to_list()
            inpout_tipo_servico = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/form[4]/table/tbody/tr[10]/td[2]/div/input')))
            for tipo_servico in tipos_servicos:
                inpout_tipo_servico.send_keys(tipo_servico)
                sleep(.5)
                inpout_tipo_servico.send_keys(Keys.RETURN)
                sleep(.5)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'submit'))).click()

            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Excel')]"))).click()

            name_file = files.check_download_name_file('consulta_servicos_')
            files.unzip_files(_dir.dir_temp)
            os.remove(os.path.join(_dir.dir_temp, name_file))
            name_file = files.check_download_name_file('consulta_servicos_')
            os.rename(os.path.join(_dir.dir_temp, name_file), os.path.join(_dir.dir_temp, 'consulta_servicos_.csv'))

            window_handles = driver.window_handles
            driver.switch_to.window(window_handles[1])
            driver.close()
            driver.switch_to.window(window_handles[0])
            driver.switch_to.default_content()

        except:
            driver.quit

    def get_prints(self):
        """
        Tira prints da tela
        """
        try:
            print('#Tirando prints')
            # Defina o nível de zoom
            driver.maximize_window()

            # Tira o print da aba Reg 1 na planilha Informe de Reguladas - STC
            driver.get("https://docs.google.com/spreadsheets/d/1M1aICDy4sxmwXsvDcvXrlKUeOgkdwjJci5Rj2IEhMBQ/edit#gid=0")
            file_reguladas_1_png = os.path.join(_dir.dir_temp, 'Reguladas1.png')
            driver.save_screenshot(file_reguladas_1_png)
            self.crop_image(55, 167, 1175, 849, file_reguladas_1_png)

            # Tira o print da aba Reg 2 na planilha Informe de Reguladas - STC
            driver.get("https://docs.google.com/spreadsheets/d/1M1aICDy4sxmwXsvDcvXrlKUeOgkdwjJci5Rj2IEhMBQ/edit#gid=1694356804")
            file_reguladas_2_png = os.path.join(_dir.dir_temp, 'Reguladas2.png')
            driver.save_screenshot(file_reguladas_2_png)
            self.crop_image(55, 171, 1175, 685, file_reguladas_2_png)

            return True
        except Exception as e:
            traceback.print_exc()
            print(e)
            return False

    def crop_image(self, x_start, y_start, x_end, y_end, img_path):
        """
        Recorta uma imagem
        """
        if not os.path.isfile(img_path):
            raise FileNotFoundError('Arquivo não encontrado')
        image = Image.open(img_path)
        box = (x_start, y_start, x_end, y_end)
        crop = image.crop(box)
        crop.save(img_path)
        return True