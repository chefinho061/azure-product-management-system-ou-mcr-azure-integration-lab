# 🛡️ MCR Cloud Assets Manager
### Sistema de Gestão de Ativos com Integração Azure SQL & Blob Storage

Este projeto consiste em uma aplicação robusta desenvolvida em **Python** e **Streamlit**, projetada para catalogar produtos e ativos diretamente na nuvem da Microsoft Azure. A solução utiliza uma arquitetura híbrida para armazenamento de dados relacionais e arquivos de mídia.

## 🚀 Funcionalidades
- **Cadastro de Ativos:** Interface intuitiva para entrada de dados (nome, descrição, preço).
- **Integração Blob Storage:** Upload automatizado de imagens com geração de UUID para evitar sobrescrita de arquivos.
- **Persistência SQL:** Armazenamento de metadados em servidor Azure SQL Database.
- **Visualização Dinâmica:** Listagem em tempo real dos itens catalogados com suporte a imagens.

## 🛠️ Stack Tecnológica
- **Frontend:** [Streamlit](https://streamlit.io/)
- **Linguagem:** Python 3.14 (Ambiente N3)
- **Database:** Azure SQL (PaaS)
- **Object Storage:** Azure Blob Storage
- **Conectividade:** `pyodbc` / `pymysql` & `azure-storage-blob`

## 📂 Estrutura do Projeto
```text
├── main.py              # Script principal da aplicação
├── .env                 # Variáveis de ambiente (Connection Strings)
├── requirements.txt     # Dependências do sistema
└── README.md            # Documentação técnica
