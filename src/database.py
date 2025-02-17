import os
import sqlite3
from app import weather_fetcher


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'weather_data.db')

def conectar_banco():
    conn = sqlite3.connect(DB_PATH)
    conn.text_factory = str
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cidade TEXT COLLATE NOCASE,
            data TEXT,
            temperatura REAL,
            umidade INTEGER,
            precipitacao REAL
        )
    """)
    conn.commit()
    return conn, cursor

def criar_tabela():
    conn, cursor = conectar_banco()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cidade TEXT,
            data TEXT,
            temperatura REAL,
            umidade INTEGER,
            precipitacao REAL
        )
    """)
    conn.commit()
    conn.close()

def buscar_clima(cidade):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""SELECT data, temperatura, umidade, precipitacao FROM weather WHERE cidade  = ? ORDER BY data DESC LIMIT 1
""", (cidade,))
    resultado = cursor.fetchone()
    
    conn.close()
    if resultado:
        data, temperatura, umidade, precipitacao = resultado

        if isinstance(data, bytes):  
            data = data.decode("utf-8")  
        
        if isinstance(temperatura, bytes):  
            temperatura = float(temperatura.decode("utf-8"))  

        if isinstance(umidade, bytes):  
            umidade = float(umidade.decode("utf-8"))  

        if isinstance(precipitacao, bytes):  
            precipitacao = float(precipitacao.decode("utf-8"))  

        return {
            "cidade": cidade,
            "data": str(data),  
            "temperatura": float(temperatura),  
            "umidade": float(umidade),
            "precipitacao": float(precipitacao)
        }
    
    return {"erro": "Cidade não encontrada"}

if __name__ == "__main__":
    criar_tabela()

def reset_database():
    conn, cursor = weather_fetcher.conectar_banco()
    cursor.execute("DELETE FROM weather WHERE cidade LIKE '%São Paulo%' OR cidade LIKE '%Sao Paulo%'")
    conn.commit()
    conn.close()
    weather_fetcher.atualizar_todas_cidades()
