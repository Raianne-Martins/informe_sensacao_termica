import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'weather_data.db')

def conectar_banco():
    return sqlite3.connect(DB_PATH)

def temperatura_media(cidade):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT AVG(temperatura) FROM weather WHERE cidade = ?
    """, (cidade,))
    
    resultado = cursor.fetchone()[0]
    conn.close()
    
    return resultado if resultado else "Nenhum dado encontrado"

def chuva_diaria_total(cidade):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT SUM(precipitacao) FROM weather WHERE cidade = ?
    """, (cidade,))
    
    resultado = cursor.fetchone()[0]
    conn.close()
    
    return resultado if resultado else "Nenhum dado encontrado"
