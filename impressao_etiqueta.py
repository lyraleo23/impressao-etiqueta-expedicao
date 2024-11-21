import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime

def gerar_root():
    root = tk.Tk()
    root.title("Impressão de Etiqueta")
    root.tk.call('source', '//10.1.1.5/j/python/ttk-theme/Forest-ttk-theme-master/forest-dark.tcl')
    ttk.Style().theme_use('forest-dark')
    root.iconbitmap('//10.1.1.5/j/python/ttk-theme/icon-Miligrama.ico')
    root.geometry("250x180")
    root.resizable(0, 0)
    return root

def preparar_romaneios():
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

    return nome_arquivo, arquivo_motoboy