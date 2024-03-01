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

import requests


class Bot:
    """_summary_: Classe que envia mensagem para o Telegram
    """
    def bot_message(self, message:str) -> requests.Response:
        # """_summary_: Envia mensagem para o Telegram

        # Args:
        #     message (str): mensagem que deseja enviar

        # Returns:
        #     _type_: retorna o status da mensagem
        # """
        bot_token = "5111702167:AAGryEfjkw7Tjqo9u8MgkX8EfZJrPdkWHDs"
        bot_chat_id = "-733624277"
        send_text = 'https://api.telegram.org/bot' + bot_token + \
            '/sendMessage?chat_id=' + bot_chat_id + '&parse_mode=Markdown&text=' + message
        try:
            response = requests.get(send_text, timeout=1000)
        except Exception as e:
            print("Erro ao enviar mnsagem do telegram:", e)
            return None
        return response.json()
        pass
