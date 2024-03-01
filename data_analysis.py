# -*- Coding: UTF-8 -*-
# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

"""
Ferramenta para analise de dados e dataframes
author: Teonas Gonçalves Dourado Netto
e-mail: teonasnetto@gmail.com
version: 1.0.0
date: 2022-02-09
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime as dt

from directories import Directories
from datetime import datetime

from gsheets import Psheets
gsheets = Psheets()

# diretorios
_dir = Directories()

class DataAnalysis:
    """_summary_: Classe que trata os arquivos de dados
    """
    def create_csv_file_send_to_gsheets(self):
        """_summary_: Cria um arquivo csv
        """
        gsheets = Psheets()

        wks_name = 'bd_config_SESMT'

        wks = gsheets.worksheet_select(wks_name, 'Bairros-UTD')
        bairros_utd = wks.get_as_df()
        wks = gsheets.worksheet_select(wks_name, 'Localidades-UTD')
        localidades_utd = wks.get_as_df()
        wks = gsheets.worksheet_select(wks_name, 'UTD-SIGLA')
        utd_sigla = wks.get_as_df()
        wks = gsheets.worksheet_select(wks_name, 'Grupos-servicos')
        grupos_servicos = wks.get_as_df()

        cols = [
            'contrato',
            'Localidade',
            'prazo_servico',
            'tipo_servico',
            'despachado',
            'Bairro',
            'Nota',
            'origem_sistema',
            'num_servico',
            'equipe'
        ]

        df = pd.read_csv(os.path.join(_dir.dir_temp, 'consulta_servicos_.csv'), encoding='utf-8', usecols=cols, sep=';', low_memory=False, keep_default_na=False)

        df = df[(df['contrato'] != '4600053669-TEC_OESTE') & (df['contrato'] != '4600053670-TEC_SUDOE')]
        df['contrato'] = df['contrato'].str[11::]
        df['Reguladas'] = df['tipo_servico'].replace(dict(zip(grupos_servicos['TIPO SERVICO'], grupos_servicos['GRUPO SERVICO'])))
        df = df[df['Reguladas'] != 'NÃO USAR']
        df.loc[df['despachado'] == 'NÃO', 'despachado'] = 'NAO'
        df['Localidade'] = df['Localidade'].str.upper()
        df['Utd'] = df['Localidade'].replace(dict(zip(localidades_utd['LOCALIDADE'], localidades_utd['UTD2'])))
        df.loc[df['Utd'] == 'FEIRA DE SANTANA', 'Utd'] = df['Bairro'].replace(dict(zip(bairros_utd['BAIRRO'], bairros_utd['UTD1'])))
        df['Data'] = df['prazo_servico'].str[0:10].str.replace('-', '/')
        df['Hora Vencimento'] = df['prazo_servico'].str[11:21]
        df = df.drop(columns=['Bairro', 'Localidade', 'prazo_servico'])
        df['Hoje'] = np.where(df['Data'] == dt.now().strftime('%d/%m/%Y'), 1, 0)
        print()
        df['equipe'] = np.where(df['equipe'] == '', 'Sem Despacho', df['equipe'])
        df['Sigla'] = df['Utd'].replace(dict(zip(utd_sigla['UTD3'], utd_sigla['SIGLA'])))
        df = df.reindex(columns=['contrato', 'origem_sistema', 'num_servico', 'Nota', 'Data', 'Hora Vencimento', 'Utd', 'Sigla', 'equipe', 'Reguladas', 'despachado', 'Hoje'])

        # Export new data to CSV file.
        df.to_csv(_dir.dir_temp + 'Teste.csv', encoding='utf-8', sep=';', index=False)

        wks = gsheets.worksheet_select('Controle acessos usuários/robôs', 'Página21')
        wks.clear(start='A2', end=f'L{wks.rows+1}')
        wks.set_dataframe(df, start='A2', copy_index=False, copy_head=False, extend=True)
