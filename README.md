# 📦 Sistema de Cadastro de Produtos - Integração Azure SQL & Blob Storage

Este repositório contém o projeto de conclusão da Atividade 01, focado na criação de uma aplicação Streamlit integrada aos serviços de nuvem da Microsoft Azure.

## 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.14 (Ambiente Experimental)
- **Frontend:** Streamlit
- **Banco de Dados:** Azure SQL Database (PaaS)
- **Armazenamento de Mídia:** Azure Blob Storage
- **Driver de Conexão:** ODBC Driver 18 for SQL Server

## 🚀 Processo de Desenvolvimento & Troubleshooting

Durante a implementação, enfrentamos e resolvemos gargalos críticos de infraestrutura híbrida:

1. **Gestão de Dependências:** Instalação modular via `pip` garantindo a presença do `pyodbc` e `azure-storage-blob`.
2. **Segurança de Rede (Firewall):** Configuração de regras de IP no Azure SQL para permitir o tráfego na porta 1433.
3. **Persistência de Dados:** Implementação de lógica para upload de imagens (Blob) seguido pela gravação de metadados no SQL.

## 💡 Insights e Aprendizados
- **Diferenciação de Drivers:** A importância de usar o driver correto (`pyodbc` vs `pymysql`). Para Azure SQL, o padrão Microsoft é mandatório.
- **Variáveis de Ambiente:** Uso do `python-dotenv` para proteger credenciais sensíveis (Connection Strings), seguindo boas práticas de segurança.
- **Ambientes Isolados:** A necessidade de validar o interpretador Python no VS Code para evitar conflitos de bibliotecas.

## 📸 Screenshots (Exemplos)
> *Dica: Tire print da sua tela do Streamlit rodando e da tabela no portal do Azure e coloque aqui.*

1. **Interface do Sistema:** ![Streamlit UI](link_da_sua_imagem)
2. **Dados no Azure SQL:** ![Azure SQL Query](link_da_sua_imagem)

---
Desenvolvido durante o curso de Gestão de Software MCR.
