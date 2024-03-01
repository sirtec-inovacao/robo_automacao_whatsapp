# -*- Coding: UTF-8 -*-
# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

"""
Ferramenta que envia dados no telegram
author: Teonas Gonçalves Dourado Netto
e-mail: teonasnetto@gmail.com
version: 1.0.0
date: 2022-02-09
"""

from directories import Directories

import os
from cryptography.fernet import Fernet
import json
from config import CHAVE_DE_CRIPTOGRAFIA

_dir = Directories()


class Decrypt:

    def decrypt_files(self, filename) -> json:
        encripted_google_key = os.path.join(_dir.dir_data, filename)
        chave = CHAVE_DE_CRIPTOGRAFIA

        cipher_suite = Fernet(chave)
        # Leia os dados criptografados do arquivo
        with open(encripted_google_key, 'rb') as arquivo_criptografado:
            dados_criptografados = arquivo_criptografado.read()
        # Descriptografe os dados
        dados_descriptografados = cipher_suite.decrypt(dados_criptografados)
        # Converta os dados descriptografados de volta para um dicionário JSON
        google_key = json.loads(dados_descriptografados)
        return google_key
