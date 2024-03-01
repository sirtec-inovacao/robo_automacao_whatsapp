import os, shutil

from datetime import datetime as dt
from datetime import timedelta as td
from time import sleep
import traceback

from web_crawler import WebCrawler
from directories import Directories
from data_analysis import DataAnalysis
from gsheets import Psheets

# diretorios
_dir = Directories()
# try:
#     shutil.rmtree(_dir.dir_temp)
# except:
#     pass
_dir.create_dir()

analysis = DataAnalysis()
scrapling = WebCrawler()

# set the title of the cmd
os.system('title Robo Automação Whatsapp')

print('######### ROBOZINHO DA BAHIA #########')

def agora():
    hora = dt.now().strftime('%H:%M')
    return hora

def hora(hora):
    convert = dt.strptime(hora, '%H:%M')
    last_convert = convert.replace(year=dt.now().year, month=dt.now().month, day=dt.now().day)
    return last_convert

def verify():
    if hora(agora()) < hora('06:00') or hora(agora()) >= hora('22:01'):
        print('O Robô estará desligado até às 06h00.')

        at_6 = (hora('06:00') - td(hours=hora(agora()).hour, minutes=hora(agora()).minute))

        sleep(((at_6.hour * 60) + at_6.minute) * 60)

def main():
    try:
        hour = dt.now().hour

        verify()

        print(dt.now().strftime('%d/%m/%Y') + '\nO Robo começou às: ' + dt.now().strftime('%Hh%M'))

        scrapling.start_chorme_driver(headless=True)
        scrapling.log_into_gpm('ba')
        scrapling.consulta_servicos_gpm()

        analysis.create_csv_file_send_to_gsheets()

        scrapling.get_prints()

        scrapling.quit_chrome_driver()

    except Exception as e:
        print(e)
        traceback.print_exc()

if __name__ == '__main__':
    main()