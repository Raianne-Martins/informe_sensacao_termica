import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime
from src.cities import CITIES

class WeatherFetcher:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.cache_path = os.path.join(self.base_dir, 'data', '.cache')
        self.db_path = os.path.join(self.base_dir, 'data', 'weather_data.db')
        cache_session = requests_cache.CachedSession(self.cache_path, expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)

    def conectar_banco(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
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
        return conn, cursor

    def obter_dados_climaticos(self, latitude, longitude, cidade):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation"],
            "timezone": "America/Sao_Paulo"
        }

        try:
            responses = self.openmeteo.weather_api(url, params=params)
            response = responses[0]

            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
            hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
            hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()

            hourly_data = {"date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            )}

            hourly_data["temperature_2m"] = hourly_temperature_2m
            hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
            hourly_data["precipitation"] = hourly_precipitation

            hourly_dataframe = pd.DataFrame(data=hourly_data)

            if not hourly_dataframe.empty:
                current_data = hourly_dataframe.iloc[0]
                self.salvar_dados(
                    cidade,
                    current_data["date"],
                    current_data["temperature_2m"],
                    current_data["relative_humidity_2m"],
                    current_data["precipitation"]
                )

                return {
                    'cidade': cidade,
                    'data': current_data["date"].strftime("%Y-%m-%d %H:%M:%S"),
                    'temperatura': float(current_data["temperature_2m"]),
                    'umidade': float(current_data["relative_humidity_2m"]),
                    'precipitacao': float(current_data["precipitation"])
                }

        except Exception as e:
            print(f"x Erro ao obter dados: {str(e)}")
            return None

    def buscar_cidade(self, cidade):
        try:
            if cidade not in CITIES:
                print(f"x Cidade '{cidade}' não encontrada")
                return None
            
            coords = CITIES[cidade]
            dados = self.obter_dados_climaticos(coords['lat'], coords['lon'], cidade)
            
            if dados:
            
                return dados
            else:
                
                return None
                
        except Exception as e:
            return None

    def salvar_dados(self, cidade, data, temperatura, umidade, precipitacao):
        conn, cursor = self.conectar_banco()
        try:
            temp = float(temperatura)
            umid = int(umidade)
            prec = float(precipitacao)
            
            current_time = data.strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute("""
                INSERT INTO weather (cidade, data, temperatura, umidade, precipitacao)
                VALUES (?, ?, ?, ?, ?)
            """, (cidade, current_time, temp, umid, prec))
            
            conn.commit()

        except Exception as e:
            print(f"x Erro ao salvar dados: {e}")
        finally:
            conn.close()

    def atualizar_todas_cidades(self):
        resultados = {}
        for cidade, coords in CITIES.items():
            dados = self.obter_dados_climaticos(coords['lat'], coords['lon'], cidade)
            if dados:
                resultados[cidade] = dados
        return resultados