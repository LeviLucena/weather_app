import os

# Configuração para SQLite
SQLALCHEMY_DATABASE_URI = "sqlite:///meu_banco.db"  # Isso cria um arquivo de banco de dados chamado "meu_banco.db"
METEOBLUE_API_KEY = os.getenv("METEOBLUE_API_KEY")
