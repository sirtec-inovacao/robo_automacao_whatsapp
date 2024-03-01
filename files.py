# -*- Coding: UTF-8 -*-
# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

"""
Ferramenta manipulação dos arquivos
author: Teonas Gonçalves Dourado Netto
e-mail: teonasnetto@gmail.com
version: 1.0.0
date: 2022-02-09
"""

import os
import time
import zipfile

from directories import Directories

# diretorios
_dir = Directories()


class Files:
    """
    Funções para manipulação de arquivos
    """

    def check_download(self, file : str, *args):
        """
        Checar se o arquivo finalizou o download através da extensão de
        tipo do chrome com inicio do nome como base
        :parameter name: parte do nome do arquivo para pesquisa
        :parameter *args: tempo máximo de loopings de 2 segundos
        que deseja aguardar o download ser realizado
        """
        print('#Aguardando download finalizar')
        app = _dir.dir_temp + file
        i = 0
        if len(args) > 0:
            total_loop = args[0]
        else:
            total_loop = 5
        while not os.path.exists(app):
            time.sleep(3)
            if i > total_loop:
                break
            i += 1

        if os.path.isfile(app):
            print('#Download finalizado')
        else:
            raise ValueError(f"{app} isn't a file!")

    def check_download_name_file(self, name):
        """
        Checar se o arquivo finalizou o download através da extensão de tipo
        do chrome com inicio do nome como base
        :parameter name: parte do nome do arquivo para pesquisa
        """
        while True:
            result = [arq for arq in os.listdir(
                _dir.dir_temp) if name in arq and ".crdownload" not in arq]
            if len(result) > 0:
                break
        print(f"Download finalizado {result[0]}")
        return result[0]

    def delete(self, str_proc:str, str_ext:str):
        """
        Procurar arquivo na pasta temporária para deleção
        :parameter strProc: Parte do nome do arquivo para pesquisa
        :parameter strProc: Extensão do arquivo
        """
        folder = _dir.dir_temp
        for file in os.listdir(folder):

            if file.find(str_proc) >= 0 and file.endswith(str_ext):
                file_path = os.path.join(folder, file)
                os.remove(file_path)

    def clear_temp(self):
        """
        Utiliza do delete() para listar os arquivos que irá limpar
        da pasta temp no inicio de cada ciclo.
        """
        print("#Deletando arquivos temporarios antigos")
        Files.delete(self, str_proc='amor', str_ext='folder')

    def unzip_files(self, folder):
        """descompacta os dados do arquivo zip para a pasta especificada

        Args:
            folder (str): path da pasta a descompactar os arquivos
        """
        files = os.listdir(_dir.dir_temp)
        files_names = []
        for file in files:
            if file.endswith('.zip'):
                filepath = _dir.dir_temp + file
                try:
                    with zipfile.ZipFile(filepath) as unzip:
                        for names in unzip.namelist():
                            files_names.append(names)
                            unzip.extract(names, folder)
                except zipfile.BadZipFile:
                    print(f"O arquivo '{file}' não é um arquivo zip válido.")
                    return 'Arquivo corrompido/inválido'

        return files_names

    def deletar_arquivo(self, str_proc='', str_ext=''):
        """
        Procurar arquivo na pasta temporária para deleção
        :parameter strProc: Parte do nome do arquivo para pesquisa
        :parameter strProc: Extensão do arquivo
        """
        folder = _dir.dir_temp
        for file in os.listdir(folder):

            if file.find(str_proc) >= 0 and file.endswith(str_ext):
                file_path = os.path.join(folder, file)
                os.remove(file_path)

    def check_file_size(self, name):
        """
        Verifica o tamanho do arquivo
        """
        for file in os.listdir(_dir.dir_temp):
            if file.startswith(name):
                file_path = _dir.dir_temp + os.sep + file
                file_size = os.path.getsize(file_path)
                return file_size
