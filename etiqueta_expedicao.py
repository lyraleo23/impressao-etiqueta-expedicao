import requests
import wget
import os
import re
import tkinter as tk
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from barcode import Code128
from barcode.writer import ImageWriter
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox
from api_miliapp import obter_tokens_tiny, get_vendas_filtro
from api_tiny_v3 import obter_notas_v3, obter_nota_fiscal_v3, obter_pedido_v3, alterar_situacao_pedido_v3
from api_intelipost import consulta_entrega_nota, obter_etiqueta
from impressao_etiqueta import gerar_root, preparar_romaneios
load_dotenv("//10.1.1.5/j/python/ttk-theme/.env")

TOKEN_TINY = str(os.getenv("TOKEN_TINY"))
TOKEN_INTELIPOST = str(os.getenv("API_KEY_INTELIPOST"))

root = gerar_root()
nome_arquivo, arquivo_motoboy = preparar_romaneios()
chaves = []

def consulta_tiny():
    global nome_arquivo

    # Armazena o input do usuário
    user_input = pedido.get()
    
    # Busca o access token da API V3 da Tiny
    origin = 'miligrama'
    ACCESS_TOKEN, REFRESH_TOKEN = obter_tokens_tiny(origin)

    # Obtém o id_pedido
    try:
        if tipo_leitor == 'Pedido':
            print('buscando pelo número do pedido...')
            numero_pedido = user_input
            nota_fiscal = None
            numero_nota = None
            params = {
                'numero_tiny': numero_pedido
            }
        elif tipo_leitor == 'Nota Fiscal':
            print('buscando pela nota fiscal...')
            nota_fiscal = None
            numero_nota = user_input
            params = {
                'numero_nota_fiscal': numero_nota
            }
        else:
            messagebox.showerror('Erro', 'Selecione o tipo de leitura!')
            return
        retorno = get_vendas_filtro(params)
        id_pedido = retorno['idPedidoTiny']
        print(f'id_pedido: {id_pedido}')
    except Exception as e:
        messagebox.showerror('Erro', f'Erro ao obter id_pedido: {e}')
        print(f'Erro ao obter id_pedido: {e}')
        id_pedido = None

    if id_pedido == None and numero_nota != None:
        try:
            params = {
               'numero': numero_nota
            }
            pesquisa_nota = obter_notas_v3(params)
            id_nota = pesquisa_nota['itens'][0]['id']
            print(f'id_nota: {id_nota}')
            nota_fiscal = obter_nota_fiscal_v3(ACCESS_TOKEN, id_nota)
            id_pedido = nota_fiscal['id_venda']
            print(f'id_pedido: {id_pedido}')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao tentar encontrar id_pedido pelo numero_nota: {e}')
            print('Erro ao tentar encontrar id_pedido pelo numero_nota')   

    # Obtém o pedido_tiny
    try:    
        if id_pedido != None:
            pedido_tiny = obter_pedido_v3(ACCESS_TOKEN, id_pedido)
            situacao = pedido_tiny['situacao']
            print(f'situacao: {situacao}')
            transportadora_tiny = pedido_tiny['transportador']['nome']
            cliente = pedido_tiny['cliente']['nome']

            if pedido_tiny != None and nota_fiscal == None:
                id_nota = pedido_tiny['idNotaFiscal']
                print(f'id_nota: {id_nota}')
                nota_fiscal = obter_nota_fiscal_v3(ACCESS_TOKEN, id_nota)
            if numero_nota == None and nota_fiscal != None:
                numero_nota = nota_fiscal['numero']
        else:
            messagebox.showerror("Erro!", "Pedido não encontrado!")
            return
    except Exception as e:
        messagebox.showerror('Erro', f'Erro ao obter pedido_tiny: {e}')
        print(f'Erro ao obter pedido_tiny: {e}')
        situacao = None

    # Não gerar etiqueta quando situacao == Cancelado
    if situacao == None or situacao == 2:
        messagebox.showerror("Cancelado", "Pedido CANCELADO na Tiny")
        return pedido.delete(0, tk.END)
    else:
        # Se a transportadora for diferente de motoboy, consulta a etiqueta na intelipost
        if transportadora_tiny not in ["VIA SANTOS EXPRESS LTDA - ME", "Ativmob"]:
            try:
                intelipost = consulta_entrega_nota(TOKEN_INTELIPOST, numero_nota)
            except requests.exceptions.Timeout:
                messagebox.showerror('Erro', 'Pedido não encontrado na intelipost')
            
            #Armazena as informações necessárias para consulta da etiqueta e geração de romaneio
            if len(intelipost['content']) == 1:
                pedido_envio = intelipost['content'][0]['order_number']
                numero_volume = intelipost['content'][0]['shipment_order_volume_array'][0]['shipment_order_volume_number']
                transportadora = intelipost['content'][0]['delivery_method_name']
                valor = intelipost['content'][0]['shipment_order_volume_array'][0]['shipment_order_volume_invoice']['invoice_total_value']
                chave = intelipost['content'][0]['shipment_order_volume_array'][0]['shipment_order_volume_invoice']['invoice_key']
                status_intelipost = intelipost['content'][0]['shipment_order_volume_array'][0]['shipment_order_volume_state']
                print('1 resultado')
            elif len(intelipost['content']) > 1:
                for x in range(0,len(intelipost['content'])):
                    content = intelipost['content'][x]
                    sales_channel = content['sales_channel']
                    print(sales_channel)
                    if sales_channel == 'RAIA_DROGASIL':
                        print('imprimir etiqueta RAIA_DROGASIL')
                        pedido_envio = content['order_number']
                        numero_volume = content['shipment_order_volume_array'][0]['shipment_order_volume_number']
                        transportadora = content['delivery_method_name']
                        valor = content['shipment_order_volume_array'][0]['shipment_order_volume_invoice']['invoice_total_value']
                        chave = content['shipment_order_volume_array'][0]['shipment_order_volume_invoice']['invoice_key']
                        status_intelipost = content['shipment_order_volume_array'][0]['shipment_order_volume_state']
            else:
                messagebox.showerror('Erro', 'Pedido não encontrado na intelipost')
                return

            print(f'status_intelipost: {status_intelipost}')
            if status_intelipost != 'CANCELLED':
                etiqueta_intelipost = obter_etiqueta(TOKEN_INTELIPOST, pedido_envio, numero_volume)
                
                #Salva o link e o nome do arquivo para armazenar
                link = etiqueta_intelipost['content']['label_url']
                
                #webbrowser.open(link)
                nome = etiqueta_intelipost['content']['order_number']
                
                wget.download(link, f"//10.1.1.5/j/python/arquivos/etiquetas/{nome}.pdf")
                pdffile = r'\\10.1.1.5\j\python\arquivos\etiquetas\{}.pdf'.format(nome)
                
                # Imprime o arquivo
                os.startfile(pdffile, 'print')
                
                #Verifica se a nota está na lista para incluir informação de duplicidade
                if chave in chaves:
                    duplicado = "Sim"
                else:
                    duplicado = "Não"
                
                #Armazena os dados em um Dataframe
                lista = f"\n{numero_nota}, {user_input}, {cliente}, {valor}, {transportadora}, {chave}, {duplicado}"
                
                with open(f'{nome_arquivo}.txt', 'a') as arquivo:
                    arquivo.write(str(lista))
                
                #Insere as chaves de nota em uma lista para verificação
                chaves.append(chave)
            else:
                messagebox.showerror('Erro', "Pedido CANCELADO na intelipost")
        # Caso seja Motoboy gera o pdf e faz a impressão da etiqueta
        elif transportadora_tiny == "Ativmob":
            # Criação de variáveis para geração do pdf
            numero_pedido = pedido_tiny['numeroPedido']
            # vendedor = pedido_tiny['nome_vendedor']
            entrega = nota_fiscal['enderecoEntrega']
            rua = entrega['endereco']
            numero = entrega['numero']
            complemento = entrega['complemento']
            bairro = entrega['bairro']
            cep = entrega['cep']
            cidade = entrega['municipio']
            uf = entrega['uf']
            telefone = pedido_tiny['cliente']['telefone']
            transportadora = pedido_tiny['transportador']['nome']
            cliente = nota_fiscal['cliente']['nome']
            valor = nota_fiscal['valor']
            chave = nota_fiscal['chaveAcesso']
            obs = pedido_tiny['observacoes']
            
            barcode = Code128(numero_pedido, writer=ImageWriter())
            barcode.save(f'//10.1.1.5/j/python/arquivos/etiquetas/barcodes/barcode_{numero_pedido}', options={"module_width":1, "module_height":40, "font_path": "//10.1.1.5/python/ttk-theme/arial.ttf"})
            
            regex = r"(.*?)\s*" + "ICMS"
            match = re.search(regex, obs, re.DOTALL)
            
            # Criação do PDF
            c = canvas.Canvas(f"//10.1.1.5/j/python/arquivos/etiquetas/{numero_nota}.pdf", pagesize=(300, 400))
            logo_miligrama = '//10.1.1.5/j/python/ttk-theme/icon-Miligrama.ico'
            barcode_i = f'//10.1.1.5/j/python/arquivos/etiquetas/barcodes/barcode_{numero_pedido}.png'
            x_start = 10
            y_start = 270
            text = c.beginText(165, 237)
            text.setFont("Helvetica", 7)
            text.textLines(f"{match.group(1)}")
            c.drawImage(logo_miligrama, x_start, y_start, width=40, preserveAspectRatio=True, mask='auto')
            c.setFont("Helvetica-Bold", 10)
            c.drawString(108, 375, f"PEDIDO {numero_pedido}")
            c.drawString(120, 360, f"NF {numero_nota}")
            c.drawImage(barcode_i, 117, 47, width=60, preserveAspectRatio=True, mask='auto')
            c.drawString(10, 165, "ATIVMOB")
            c.drawString(10, 205, "ATIVMOB - FORTALEZA")
            c.drawString(10, 300, "DESTINATÁRIO")
            # c.drawString(10, 130, f"{vendedor}")
            c.drawString(10, 105, f"{telefone}")
            c.drawString(275,165, "1/1")
            c.setFont("Helvetica", 9)
            c.drawString(10, 285, f"{cliente}")
            c.drawString(10, 273, f"{rua}, {numero}")
            c.drawString(10, 260, f"{complemento}, {bairro}")
            c.drawString(10, 247, f"{cidade}, {uf}")
            c.drawString(10, 235, f"{cep}")
            c.drawString(10, 215, "Forma de Envio")
            c.drawString(10, 180, "Transportadora")
            # c.drawString(10, 140, "Vendedor")
            c.drawString(10, 115, "Telefone")
            c.drawString(258,180, "Volume")
            c.drawString(165,247, "Obs:")
            c.drawString(70,40, "Assinatura")
            c.drawString(235,40, "Data")
            c.drawText(text)
            c.line(5, 50, 180, 50)
            c.line(200, 50, 290, 50)
            c.line(230, 50, 232, 65)
            c.line(260, 50, 262, 65)
            c.save()
            
            # Cria uma variável com o caminho do arquivo
            pdffile = r'\\10.1.1.5\j\python\arquivos\etiquetas\{}.pdf'.format(numero_nota)
            
            # Imprime o arquivo
            os.startfile(pdffile, 'print')
            
            #Verifica se a nota está na lista para incluir informação de duplicidade
            if chave in chaves:
                duplicado = "Sim"
            else:
                duplicado = "Não"
            
            #Armazena os dados em um Dataframe
            lista = f"\n{numero_nota}, {user_input}, {cliente}, {valor}, {transportadora}, {chave}, {duplicado}"
            
            #Edita o arquivo de texto para incluir as informações do pedido
            with open(f'{nome_arquivo}.txt', 'a') as arquivo:
                arquivo.write(str(lista))
            
            #Alterar a situação
            alterar_situacao_pedido_v3(ACCESS_TOKEN, id_pedido, 5)
            
            #Insere as chaves de nota em uma lista para verificação
            chaves.append(chave)
        else:
            # Criação de variáveis para geração do pdf
            numero_pedido = pedido_tiny['numeroPedido']
            # vendedor = pedido_tiny['nome_vendedor']
            entrega = nota_fiscal['enderecoEntrega']
            rua = entrega['endereco']
            numero = entrega['numero']
            complemento = entrega['complemento']
            bairro = entrega['bairro']
            cep = entrega['cep']
            cidade = entrega['municipio']
            uf = entrega['uf']
            telefone = pedido_tiny['cliente']['telefone']
            transportadora = pedido_tiny['transportador']['nome']
            cliente = nota_fiscal['cliente']['nome']
            valor = nota_fiscal['valor']
            chave = nota_fiscal['chaveAcesso']
            obs = pedido_tiny['observacoes']
            forma_envio = pedido_tiny['transportador']['formaFrete']['nome']
            bairros = {
                'Abranches': 20,
                'Água Verde': 13,
                'Ahú': 13,
                'Alto Boqueirão': 21,
                'Alto da Glória': 13,
                'Alto da Rua XV': 13,
                'Atuba': 21,
                'Augusta': 21,
                'Bacacheri': 16,
                'Bairro Alto': 20,
                'Barreirinha': 20,
                'Batel': 13,
                'Bigorrilho': 13,
                'Boa Vista': 20,
                'Bom Retiro': 13,
                'Boqueirão': 16,
                'Butiatuvinha': 21,
                'Cabral': 16,
                'Cachoeira': 23,
                'Cajuru': 20,
                'Campina do Siqueira': 16,
                'Campo Comprido': 20,
                'Campo de Santana': 21,
                'Capão da Imbuia': 20,
                'Capão Raso': 20,
                'Cascatinha': 20,
                'Centro': 13,
                'Caximba': 21,
                'Centro Cívico': 13,
                'Cidade Industrial': 21,
                'Cristo Rei': 13,
                'Fanny': 13,
                'Fazendinha': 20,
                'Ganchinho': 21,
                'Guabirotuba': 16,
                'Guaíra': 13,
                'Hauer': 16,
                'Hugo Lange': 16,
                'Jardim Botânico': 16,
                'Jardim Social': 16,
                'Jardim das Américas': 20,
                'Juvevê': 16,
                'Lamenha Pequena': 23,
                'Lindóia': 13,
                'Mercês': 13,
                'Mossunguê': 20,
                'Novo Mundo': 16,
                'Orleans': 20,
                'Parolin': 13,
                'Pilarzinho': 16,
                'Pinheirinho': 20,
                'Portão': 16,
                'Rebouças': 13,
                'Riviera': 21,
                'Santa Cândida': 21,
                'Santa Felicidade': 20,
                'Santa Quitéria': 16,
                'Santo Inácio': 20,
                'São Braz': 20,
                'São Francisco': 13,
                'São João': 20,
                'São Lourenço': 20,
                'São Miguel': 21,
                'Seminário': 16,
                'Sítio Cercado': 21,
                'Taboão': 20,
                'Tarumã': 20,
                'Tatuquara': 21,
                'Tingui': 20,
                'Uberaba': 16,
                'Umbará': 21,
                'Vila Izabel': 13,
                'Vista Alegre': 16,
                'Xaxim': 16
            }
            cidades = {
                'Almirante Tamandaré': 30,
                'Araucária': 35,
                'Campo Largo': 40,
                'Colombo': 35,
                'Fazenda Rio Grande': 35,
                'Pinhais': 25,
                'Piraquara': 30,
                'São José dos Pinhais': 30,
                'Campo Magro': 30
            }
            
            # Valida se a Entrega é em Curitiba, se não for consulta valores para outras cidades
            if cidade == 'Curitiba':
                valor_motoboy = bairros[bairro]
            else:
                valor_motoboy = cidades[cidade]
            
            barcode = Code128(numero_pedido, writer=ImageWriter())
            barcode.save(f'//10.1.1.5/j/python/arquivos/etiquetas/barcodes/barcode_{numero_pedido}', options={"module_width":1, "module_height":40, "font_path": "//10.1.1.5/python/ttk-theme/arial.ttf"})
            
            # Criação do PDF
            regex = r"(.*?)\s*" + "ICMS"
            match = re.search(regex, obs, re.DOTALL)
            c = canvas.Canvas(f"//10.1.1.5/j/python/arquivos/etiquetas/{numero_nota}.pdf", pagesize=(300, 400))
            logo_miligrama = '//10.1.1.5/j/python/ttk-theme/icon-Miligrama.ico'
            barcode_i = f'//10.1.1.5/j/python/arquivos/etiquetas/barcodes/barcode_{numero_pedido}.png'
            x_start = 10
            y_start = 270
            text = c.beginText(165, 237)
            text.setFont("Helvetica", 7)
            text.textLines(f"{match.group(1)}")
            c.drawImage(logo_miligrama, x_start, y_start, width=40, preserveAspectRatio=True, mask='auto')
            c.setFont("Helvetica-Bold", 10)
            c.drawString(108, 375, f"PEDIDO {numero_pedido}")
            c.drawString(120, 360, f"NF {numero_nota}")
            c.drawImage(barcode_i, 117, 47, width=60, preserveAspectRatio=True, mask='auto')
            c.drawString(10, 165, "VIA SANTOS EXPRESS LTDA - ME")
            c.drawString(10, 205, f"{forma_envio}")
            c.drawString(10, 300, "DESTINATÁRIO")
            # c.drawString(10, 130, f"{vendedor}")
            c.drawString(10, 105, f"{telefone}")
            c.drawString(275,165, "1/1")
            c.setFont("Helvetica", 9)
            c.drawString(10, 285, f"{cliente}")
            c.drawString(10, 273, f"{rua}, {numero}")
            c.drawString(10, 260, f"{complemento}, {bairro}")
            c.drawString(10, 247, f"{cidade}, {uf}")
            c.drawString(10, 235, f"{cep}")
            c.drawString(10, 215, "Forma de Envio")
            c.drawString(10, 180, "Transportadora")
            # c.drawString(10, 140, "Vendedor")
            c.drawString(10, 115, "Telefone")
            c.drawString(258,180, "Volume")
            c.drawString(165,247, "Obs:")
            c.drawString(70,40, "Assinatura")
            c.drawString(235,40, "Data")
            c.drawText(text)
            c.line(5, 50, 180, 50)
            c.line(200, 50, 290, 50)
            c.line(230, 50, 232, 65)
            c.line(260, 50, 262, 65)
            c.save()
            
            # Cria uma variável com o caminho do arquivo
            pdffile = r'\\10.1.1.5\j\python\arquivos\etiquetas\{}.pdf'.format(numero_nota)
            
            # Imprime o arquivo
            os.startfile(pdffile, 'print')
            
            #Verifica se a nota está na lista para incluir informação de duplicidade
            if chave in chaves:
                duplicado = "Sim"
            else:
                duplicado = "Não"
            
            #Armazena os dados em um Dataframe
            lista = f"\n{numero_nota}, {user_input}, {cliente}, {cidade}, {bairro}, {valor_motoboy}, {forma_envio}"
            
            #Edita o arquivo de texto para incluir as informações do pedido
            with open(f'{arquivo_motoboy}.txt', 'a') as arquivo:
                arquivo.write(str(lista))
            
            #Alterar a situação
            alterar_situacao_pedido_v3(ACCESS_TOKEN, id_pedido, 5)
            
            #Insere as chaves de nota em uma lista para verificação
            chaves.append(chave)
    pedido.delete(0, tk.END)

def acionar_botao(event):
    consulta_tiny()

def tipo(event):
    global tipo_leitor
    tipo_leitor = options.get()

#Seleção de tipo leitura de pedido ou nota
options = ttk.Combobox(root, state='readonly', values=['Pedido', 'Nota Fiscal'])
options.bind("<<ComboboxSelected>>", tipo)
options.grid(row=1, column=1)

tipo_leitura = tk.Label(root, text='Selecione pedido ou nota fiscal')
tipo_leitura.grid(row=0, column=1)

#Label do pedido
label_pedido = tk.Label(root, text="Digite o número do pedido")
# label_pedido.place(x=40 , y=50)
label_pedido.grid(row=5, column=1)

#Variável para obter input do usuário
pedido = tk.Entry(root)
# pedido.place(x=40 , y=75)
pedido.grid(row=6, column=1)

# Vincula o evento de pressionar a tecla Enter à janela principal
root.bind('<Return>', acionar_botao)

root.mainloop()
