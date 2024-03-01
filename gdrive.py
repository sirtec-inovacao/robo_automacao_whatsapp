# -*- Coding: UTF-8 -*-
# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

"""
Ferramenta gerencia e manipula o drive do google
author: Teonas Gonçalves Dourado Netto
e-mail: teonasnetto@gmail.com
version: 1.0.0
date: 2022-02-09
"""

import os

from pydrive2.auth import GoogleAuth, ServiceAccountCredentials
from pydrive2.drive import GoogleDrive
from decrypt import Decrypt


class GDrive():
    """Classe para manipular arquivos no google drive"""

    def __init__(self, dir_data: str, account_type: str):
        self.dir_data = dir_data
        self.account_type = account_type
        self.drive = None

        if os.path.isfile(os.path.join((self.dir_data), 'chaveGoogle')):
            if account_type == "service_account":
                GDrive.drive_auth_service_account(self, dir_data=self.dir_data)
            elif account_type == "google_account":
                GDrive.drive_auth_google_account(self)
            else:
                raise Exception("Login account type not supported")
        else:
            raise Exception("Google account key not found")

    def drive_auth_service_account(self, dir_data):
        """_summary_ : Autenticação com a conta de serviço do google drive

        Args:
            dir_data (_type_): diretorio onde deve se encontar o arquivo chaveGoogle.json
        """
        gauth = GoogleAuth()
        scope = "https://www.googleapis.com/auth/drive"
        gauth.auth_method = 'service'
        google_key = Decrypt().decrypt_files('chaveGoogle')
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            google_key, scope)
        self.drive: GoogleDrive = GoogleDrive(gauth)

    def drive_auth_google_account(self):
        """_summary_ : Autenticação com a conta do google drive"""
        gauth = GoogleAuth()
        # autenticar com o google account and refresh token
        gauth.LoadCredentialsFile("mycreds.txt")
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile("mycreds.txt")

        drive = GoogleDrive(gauth)

        return drive

    def _show_quota(self):
        """Mostra o espaço utilizado no google drive"""
        about = self.drive.GetAbout()
        print(f"Current user name:{about['name']}")
        print(f"Root folder ID:{about['rootFolderId']}")
        print(f"Total quota (bytes):{about['quotaBytesTotal']}")
        print(f"Used quota (bytes):{about['quotaBytesUsed']}")

    def _list_files(self):
        """Lista os arquivos do google drive"""
        # file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        file_list = self.drive.ListFile({"q": 'trashed=false'}).GetList()
        for file1 in file_list:
            print(f"title: {file1['title']}, id: {file1['id']}")

    def _create_file(self, title, folder_id):
        """_summary_ : Cria um arquivo no google drive

        Args:
            title (_type_): titulo do arquivo
            folder_id (_type_): id da pasta onde o arquivo será criado
        """
        # Create GoogleDriveFile instance with title 'Hello.txt'.
        file1 = self.drive.CreateFile(
            {"parents": [{"kind": "drive#fileLink", "id": folder_id}], 'title': title})
        # Set content of the file from given string.
        file1.SetContentString('')
        file1.Upload()

    def _list_folders(self, folder_id):
        """Lista as pastas do google drive"""
        folders_id = {}
        file_list = self.drive.ListFile(
            {"q": f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
        for file1 in file_list:
            print(f"Folder: {file1['title']}, id: {file1['id']}")
            folders_id.update({file1['title']: file1['id']})

        return folders_id

    def _list_folder_content(self, folder_id) -> dict:
        """_summary_ : Lista os arquivos de uma pasta

        Args:
            folder_id (_type_): id da pasta

        Returns:
            dict: dicionario com os arquivos da pasta
        """
        files_name_id = {}
        file_list = self.drive.ListFile(
            {'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            print(f"Folder: {file1['title']}, id: {file1['id']}")
            files_name_id.update({file1['title']: file1['id']})
        return files_name_id

    def _upload_file(self, file, title, folder_name, is_id=False):
        """_summary_ : Faz o upload de um arquivo para o google drive

        Args:
            file (_type_): arquivo a ser enviado
            title (_type_): titulo do arquivo
            folder_name (_type_): nome da pasta onde o arquivo será enviado
            id (bool, optional): se o nome da pasta no folder_name for um ID. Defaults to False.
        """
        try:
            if is_id is False:
                if os.path.isfile(file):
                    folders = self.drive.ListFile(
                        {'q': f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList() # pylint: disable=line-too-long

                    for folder in folders:
                        if folder['title'] == folder_name:
                            file2 = self.drive.CreateFile(
                                {'parents': [{'id': folder['id']}], 'title': title})
                            file2.SetContentFile(file)
                            file2.Upload()
            elif is_id is True:
                file2 = self.drive.CreateFile(
                    {"parents": [{"kind": "drive#fileLink", "id": folder_name}], 'title': title})
                file2.SetContentFile(file)
                file2.Upload()
        except Exception as _e: # pylint: disable=broad-except
            print(_e)

    def _overwrite_file(self, file, title, folder_id):
        file_list = self.drive.ListFile(
            {'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
        try:
            for file1 in file_list:
                if file1['title'] == title:
                    file1.Trash()
                    _f = self.drive.CreateFile(
                        {'parents': [{'id': folder_id}], 'title': title})
                    _f.SetContentFile(file)
                    _f.Upload()
                else:
                    pass
        except Exception as _e: # pylint: disable=broad-except
            print(_e)

    def _create_folder(self, folder_name, parent_folder_id):
        # Create folder.
        folder_metadata = {
        "title": f"{folder_name}",
        # The mimetype defines this new file as a folder, so don't change this.
        "mimeType": "application/vnd.google-apps.folder",
        'parents': [{'id': parent_folder_id}]
        }
        folder = self.drive.CreateFile(folder_metadata)
        folder.Upload()

        # Get folder info and print to screen.
        folder_title = folder["title"]
        folder_id = folder["id"]
        print(f"title: {folder_title}, id: {folder_id}")

        return folder

    def _delete_file(self, file_id):
        file = self.drive.CreateFile({'id': file_id})
        file.Delete()

    def _trash_file(self, file_id):
        file = self.drive.CreateFile({'id': file_id})
        file.Trash()

    def _download_file(self, file_id, folder_to_save):
        file = self.drive.CreateFile({'id': file_id})
        file.GetContentFile(folder_to_save)
