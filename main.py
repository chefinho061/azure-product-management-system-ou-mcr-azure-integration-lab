import streamlit as st
from azure.storage.blob import BlobServiceClient
import os 
import pymysql
import uuid
from dotenv import load_dotenv

# --- CONFIGURAÇÃO DA IDENTIDADE VISUAL ---
st.set_page_config(page_title="MCR - Cloud Catalog", page_icon="📦", layout="wide")

# Inicialização de variáveis de ambiente
load_dotenv()

# Credenciais Cloud
BLOB_CONN = os.getenv("BLOB_CONNECTIOPN_STRING")
BLOB_CONT = os.getenv("BLOB_CONTAINER_NAME")
BLOB_ACC = os.getenv("BLOB_ACCOUNT_NAME")

DB_HOST = os.getenv("SQL_SERVER")
DB_NAME = os.getenv("SQL_DATABASE")
DB_USER = os.getenv("SQL_USER")
DB_PASS = os.getenv("SQL_PASSWORD")

# --- MÓDULO DE INFRAESTRUTURA (Lógica Única) ---

def azure_cloud_integration(image_file):
    """Gerencia o upload para o Blob Storage com tratamento de erro."""
    try:
        service_client = BlobServiceClient.from_connection_string(BLOB_CONN)
        container_client = service_client.get_container_client(BLOB_CONT)
        
        # Gerar identificador único MCR
        unique_name = f"mcr_product_{uuid.uuid4().hex[:8]}_{image_file.name}"
        blob_client = container_client.get_blob_client(unique_name)
        
        blob_client.upload_blob(image_file.read(), overwrite=True)
        return f"https://{BLOB_ACC}.blob.core.windows.net/{BLOB_CONT}/{unique_name}"
    except Exception as e:
        st.error(f"Falha Crítica no Blob Storage: {e}")
        return None

def db_transaction_handler(p_name, p_desc, p_price, p_url):
    """Executa a transação SQL garantindo o fechamento da conexão."""
    try:
        conn = pymysql.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, 
            database=DB_NAME, cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # SQL parametrizado para evitar SQL Injection
            sql = "INSERT INTO produtos (name, descricao, preco, image_url) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (p_name, p_desc, p_price, p_url))
        conn.commit()
        conn.close()
        return True
    except pymysql.MySQLError as err:
        st.error(f"Erro de Banco de Dados [MCR-SQL]: {err}")
        return False

# --- INTERFACE DE USUÁRIO (CUSTOM) ---

st.title("🛡️ Sistema de Gestão de Ativos - MCR")
st.subheader("Integração Híbrida: Azure SQL + Blob Storage")

col1, col2 = st.columns([1, 1])

with col1:
    st.info("Formulário de Entrada de Dados")
    name = st.text_input("Etiqueta do Produto", placeholder="Ex: Câmera Industrial")
    desc = st.text_area("Especificações Técnicas", placeholder="Descreva os detalhes do hardware...")
    price = st.number_input("Valor de Ativo (R$)", min_value=0.0)
    file = st.file_uploader("Evidência Visual (Imagem)", type=["png", "jpg", "jpeg"])

with col2:
    st.info("Status de Sincronização")
    if st.button("🚀 Processar e Sincronizar com Azure"):
        if name and file:
            with st.spinner("Estabelecendo conexão com Azure Cloud..."):
                # Etapa 1: Blob
                image_url = azure_cloud_integration(file)
                
                if image_url:
                    # Etapa 2: SQL
                    success = db_transaction_handler(name, desc, price, image_url)
                    
                    if success:
                        st.toast("Dados replicados com sucesso!", icon='✅')
                        st.success(f"Ativo '{name}' catalogado na nuvem.")
                        st.balloons()
        else:
            st.warning("⚠️ Erro de Validação: Nome e Imagem são campos obrigatórios.")

# --- SEÇÃO DE LISTAGEM ---
st.markdown("---")
if st.checkbox("🔍 Visualizar Catálogo de Produtos"):
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        with conn.cursor() as cursor:
            cursor.execute("SELECT name, descricao, preco, image_url FROM produtos")
            data = cursor.fetchall()
            for row in data:
                with st.expander(f"Produto: {row[0]}"):
                    st.write(f"**Preço:** R$ {row[2]}")
                    st.write(f"**Descrição:** {row[1]}")
                    st.image(row[3], width=200)
        conn.close()
    except Exception as e:
        st.write(f"Aguardando sincronização de dados... Erro: {e}")