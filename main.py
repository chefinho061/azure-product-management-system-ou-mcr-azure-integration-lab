import streamlit as st
from azure.storage.blob import BlobServiceClient
import os 
import pymysql
import uuid
import json


from dotenv import load_dotenv
load_dotenv()  # Carrega as variáveis do seu arquivo .env
BlobConnectionString = os.getenv("BLOB_CONNECTIOPN_STRING")
BlobContainerName = os.getenv("BLOB_CONTAINER_NAME")
Blobaccountname = os.getenv("BLOB_ACCOUNT_NAME")

SQL_Server = os.getenv("SQL_SERVER")
SQL_Database = os.getenv("SQL_DATABASE")
SQL_User = os.getenv("SQL_USER")
SQL_Password = os.getenv("SQL_PASSWORD")

st.title("cadastro de produtos")
#formulário para cadastro de produtos
product_name = st.text_input("Nome do produto")
product_description = st.text_area("Descrição do produto")
product_price = st.number_input("Preço do produto", min_value=0.0, format="%.2f")
product_image = st.file_uploader("Imagem do produto", type=["jpg", "jpeg", "png"])

#salvar produto no banco de dados e imagem no blob storage

def upload_image_to_blob(image_file):
    blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
    container_client = blob_service_client.get_container_client(BlobContainerName)
    blob_name = f"{uuid.uuid4()}_{image_file.name}"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(image_file.read(), overwrite=True)
    image_url = f"https://{Blobaccountname}.blob.core.windows.net/{BlobContainerName}/{blob_name}"
    return image_url


def insert_product(product_name, product_description, product_price, image_url):
    connection = pymysql.connect(
        host=SQL_Server,
        user=SQL_User,
        password=SQL_Password,
        database=SQL_Database
    )
    cursor = connection.cursor()
    cursor.execute("insert into products (nome, descricao, preco, image_url) values (%s, %s, %s, %s)", (product_name, product_description, product_price, image_url))
    try:
        with connection.cursor() as cursor:
            insert_sql = "INSERT INTO produtos (name, descricao, preco, image_url) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_sql, (product_name, product_description, product_price, image_url))
        connection.commit()
    finally:
        connection.close()

def list_products():
    connection = pymysql.connect(
        host=SQL_Server,
        user=SQL_User,
        password=SQL_Password,
        database=SQL_Database
    )
    cursor = connection.cursor()
    cursor.execute("SELECT name, descricao, preco, image_url FROM produtos")
    products = cursor.fetchall()
    connection.close()
    return products

if st.button("Salvar produto"):
    insert_product(product_name, product_description, product_price, upload_image_to_blob(product_image))
    return_message = "Produto salvo com sucesso!"

    st.header("Produto cadastrado:")
    if st.button("Listar produtos"):
        return_message = "Produtos listados com sucesso!"
