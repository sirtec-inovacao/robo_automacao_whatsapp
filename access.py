# -*- Coding: UTF-8 -*-
# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

"""
Ferramenta os acessos no arquivo de configuração
author: Teonas Gonçalves Dourado Netto
e-mail: teonasnetto@gmail.com
version: 1.0.0
date: 2022-02-09
"""

import pandas as pd
from gsheets import Psheets

gsheets = Psheets()

class Access:
    """_summary_: Classe que retorna os acessos
    """
    def __init__(self):
        wks = gsheets.worksheet_select('bd_config_SESMT', 'access')
        wks.get_all_records()
        self.config_df = pd.DataFrame(wks.get_all_records(numericise_data=False), dtype=str)

        self.login_gpm = self.config_df.loc[self.config_df['local']=='TESTE']["login"].values[0]
        self.passw_gpm = self.config_df.loc[self.config_df['local']=='TESTE']["passw"].values[0]
