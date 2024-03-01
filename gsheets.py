# -*- Coding: UTF-8 -*-
# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

"""
Ferramenta para atualização de dados no Google Sheets
author: Teonas Gonçalves Dourado Netto
e-mail: teonasnetto@gmail.com
version: 1.0.0
date: 2022-02-09
"""

import os

import pygsheets
from pandas import DataFrame
from pygsheets import Worksheet

from google.oauth2 import service_account
from decrypt import Decrypt

class Psheets:
    """_summary_: Calsse que atualiza planilha no Google Sheets
    """

    def worksheet_select(self, plan : str, title : str) -> Worksheet:
        """_summary_: Seleciona planilha no Google Sheets

        Args:
            plan (str): nome da planilha
            title (str): título da planilha

        Returns:
            Worksheet: retorna um objeto Worksheet
        """
        print('abrindo plan online')

        google_key = Decrypt().decrypt_files('chaveGoogle')

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_info(google_key, scopes=SCOPES)
        _gc = pygsheets.authorize(custom_credentials=credentials)
        _sh = _gc.open(plan)
        wks = _sh.worksheet(property='title', value=title)  # type: ignore
        return wks

    def _worksheet_clear(self, wks : Worksheet):
        """_summary_: Limpa planilha no Google Sheets

        Args:
            wks (Worksheet): a planilha que deseja limpar
        """
        print('limpando plan online')
        wks.clear()

    def _worksheet_update(self, wks:Worksheet, _df:DataFrame):
        """_summary_: Atualiza planilha no Google Sheets

        Args:
            wks (Worksheet): a planilha que deseja atualizar
            df (DataFrame): dataframe com os dados
        """
        print('enviando dados plan online')
        wks.set_dataframe(_df, (1, 1))

    def worksheet_append(self, wks:Worksheet, _df:DataFrame):
        """_summary_: Adiciona dados no final da planilha no Google Sheets

        Args:
            wks (Worksheet): a planilha que deseja atualizar
            df (DataFrame): dataframe com os dados
        """
        print('enviando dados plan online')
        wks.set_dataframe(_df, (wks.rows+1, 1), extend=True, copy_head=False)
