# 🏷️ Impressão de Etiquetas de Expedição

## 📋 Descrição

Este projeto tem como objetivo **gerar e imprimir etiquetas de expedição** para transportadoras,  
utilizando a **API da Intelipost** sempre que possível. Caso a API não esteja disponível  
ou a transportadora não seja suportada, o programa cria uma **etiqueta própria** de forma personalizada.

🔹 **Fluxo de funcionamento:**  
1. Consulta a API da **Intelipost** para gerar a etiqueta da transportadora.  
2. Se a API não estiver disponível, cria uma **etiqueta alternativa**.  
3. Gera um arquivo pronto para impressão.  

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.  
- **Bibliotecas Principais**:
  - `requests` → Comunicação com a API da Intelipost.  
  - `reportlab` → Geração de etiquetas personalizadas em PDF.  
  - `dotenv` → Gerenciamento de variáveis de ambiente.  


## 🚀 Como Utilizar o Projeto

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/lyraleo23/impressao-etiqueta-expedicao.git
cd impressao-etiqueta-expedicao
```

### Passo 2: Instalar Dependências
Certifique-se de ter o Python instalado. Depois, instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

### Passo 3: Configurar Variáveis de Ambiente
Crie um arquivo `.env` e configure suas credenciais da API da Intelipost:
```bash
INTELIPOST_API_KEY
TOKEN_MILIAPP
```

### Passo 4: Executar o Script Principal
```bash
python main.py
```

### Passo 5: Verificar a Etiqueta Gerada
O arquivo gerado estará salvo na pasta etiquetas/ pronto para impressão.

### 📄 Estrutura do Projeto  
```markdown
📂 impressao-etiqueta-expedicao  
 ├── main.py              # Script principal para geração das etiquetas  
 ├── requirements.txt     # Dependências do projeto  
 ├── README.md            # Documentação do projeto  
 ├── .env.example         # Exemplo do arquivo de configuração  
 ├── input/               # Pasta de entrada de pedidos  
 ├── output/              # Pasta onde serão salvas as etiquetas geradas  
 ├── utils.py             # Funções auxiliares para formatação e impressão  
 ├── api_intelipost.py    # Módulo para comunicação com a API da Intelipost  
 ├── etiqueta_custom.py   # Módulo para geração de etiquetas personalizadas  
 └── templates/           # Modelos de etiquetas personalizadas  
```

## 🧠 Conceitos Aplicados

- **Integração com API da Intelipost** → Obtenção de etiquetas oficiais.  
- **Geração de PDF com ReportLab** → Criação de etiquetas personalizadas.  
- **Automação de Processos** → Impressão e gerenciamento de arquivos.  

## 📄 Licença

Este projeto está sob a licença MIT.

## 🤝 Contribuições

Contribuições são bem-vindas! Caso encontre melhorias ou precise relatar problemas,  
sinta-se à vontade para abrir issues ou pull requests.

## 📞 Contato

- **Autor**: Leonardo Lyra  
- **GitHub**: [lyraleo23](https://github.com/lyraleo23)  
- **LinkedIn**: [Leonardo Lyra](https://www.linkedin.com/in/leonardo-lyra/)  

