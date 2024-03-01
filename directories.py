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

import os
import sys

class Directories:
    """_summary_: Classe que cria e retorna os diretorios
    """

    def get_current_directory(self):
        if getattr(sys, 'frozen', False):  # Verifique se o script está congelado (como um executável .exe)
            # Se sim, obtenha o diretório do executável
            exe_path = sys.executable
            return os.path.dirname(os.path.abspath(exe_path))
        else:
            # Caso contrário, obtenha o diretório do arquivo .py atual
            return os.path.dirname(os.path.abspath(__file__))


    def __init__(self):
        self.dir_path = self.get_current_directory() + os.path.sep
        self.dir_app = os.path.join(self.dir_path + 'app')
        self.dir_data = os.path.join(self.dir_path + 'app\\data\\')
        self.dir_images = os.path.join(self.dir_path + 'app\\images\\')
        self.dir_temp = os.path.join(self.dir_path + 'app\\temp\\')
        self.dir_cache = os.path.join(self.dir_path + 'app\\data\\cache\\')
        self.dir_log = os.path.join(self.dir_path + 'app\\log\\')

        os.chdir(self.dir_path)

    def create_dir(self):
        """_summary_: Cria os diretorios
        """
        dirs = [self.dir_app, self.dir_data, self.dir_images,
            self.dir_temp, self.dir_cache, self.dir_log]
        for _dir in dirs:
            if not os.path.exists(_dir):
                os.makedirs(_dir)
