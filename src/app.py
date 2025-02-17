import sqlite3
from flask import Flask , request, jsonify, render_template , send_from_directory
from src.fetch_data import WeatherFetcher
from src.cities import CITIES

app = Flask(__name__,  template_folder='../templates', 
    static_folder='../static'   )
weather_fetcher = WeatherFetcher()

CITIES = ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Curitiba", "Santos", "Belo Horizonte", "Recife", "Aparecida"]

@app.route("/buscar")
def buscar():
    cidade = request.args.get("cidade")
    
    if not cidade:
        return jsonify({"error": "Cidade não especificada"})
    
    try:
        dados_api = weather_fetcher.buscar_cidade(cidade)
        if dados_api:
            sensacao_termica = calculate_heat_index(dados_api['temperatura'], dados_api['umidade'])
            dados_api['sensacao_termica'] = round(sensacao_termica, 1)
            return jsonify(dados_api)
        else:
            return jsonify({"error": "Cidade não encontrada"})
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar dados: {str(e)}"}), 500


def calculate_heat_index(temperature, humidity):
   
    temp_f = (temperature * 9/5) + 32
    
    hi = 0.5 * (temp_f + 61.0 + ((temp_f - 68.0) * 1.2) + (humidity * 0.094))
    
    if hi > 80:
        hi = -42.379 + 2.04901523 * temp_f + 10.14333127 * humidity
        hi = hi - 0.22475541 * temp_f * humidity
        hi = hi - 6.83783e-3 * temp_f**2
        hi = hi - 5.481717e-2 * humidity**2
        hi = hi + 1.22874e-3 * temp_f**2 * humidity
        hi = hi + 8.5282e-4 * temp_f * humidity**2
        hi = hi - 1.99e-6 * temp_f**2 * humidity**2
     
    return (hi - 32) * 5/9

@app.route('/cidades')
def cidades():
    return jsonify(CITIES)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/cidades")
def listar_cidades():
    """Return list of available cities."""
    return jsonify(list(CITIES.keys()))

@app.route('/weather/<cidade>')
def get_weather(cidade):
    dados = weather_fetcher.buscar_cidade(cidade)
    if dados:
        return jsonify(dados)
    return jsonify({"error": "Cidade não encontrada"}), 404

if __name__ == "__main__":
    weather_fetcher.atualizar_todas_cidades()
    app.run(debug=True)