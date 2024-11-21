import os
import wget
import re
import tkinter as tk
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from barcode import Code128
from barcode.writer import ImageWriter
from datetime import datetime
from tkinter import ttk, messagebox
from api_miliapp import obter_tokens_tiny
from impressao_etiqueta import gerar_root

load_dotenv("//10.1.1.5/j/python/ttk-theme/.env")

TOKEN_TINY = str(os.getenv("TOKEN_TINY"))
API_INTELIPOST = str(os.getenv("API_KEY_INTELIPOST"))


def main():
    origin = 'miligrama'
    ACCESS_TOKEN, REFRESH_TOKEN = obter_tokens_tiny(origin)

    root = gerar_root()

    dados = "Número NF, Número Pedido, Destinatário, Valor, Transportadora, Chave NFe, Duplicado"

    hoje = datetime.now()
    hoje_str = str(hoje)
    data = hoje_str[:10]
    hora = hoje_str[11:]
    hora = hora.replace(":", "-")
    hora = hora[:8]

    #Define os dados para a criação do arquivo com as informações da transportadora
    caminho = f"//10.1.1.5/j/python/arquivos/etiquetas/Romaneios/{data}"
    nome_arquivo = caminho + f"/Romaneio-{hora}"

    #Define os dados para a criação do arquivo com as informações do motoboy
    dados_motoboy = "Número NF, Número Pedido, Cliente, Cidade, Bairro, Valor Motoboy, Período"
    arquivo_motoboy = caminho + f"/motoboy-romaneio-{hora}"

    # Verifica se a pasta já existe
    if not os.path.exists(caminho):
        os.makedirs(caminho)

    # Insere o cabeçalho no arquivo motoboy
    with open(f'{arquivo_motoboy}.txt', 'w') as arquivomotoboy:
        arquivomotoboy.write(str(dados_motoboy))

    # Insere o cabeçalho no arquivo transportadoras
    with open(f'{nome_arquivo}.txt', 'w') as arquivo:
        arquivo.write(str(dados))
    
    chaves = []

    