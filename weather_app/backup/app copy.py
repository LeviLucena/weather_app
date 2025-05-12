# APP SEM FILTO DE DATA, APENAS SEMANA ATUAL
from flask import Flask, render_template, request, jsonify
from config import SQLALCHEMY_DATABASE_URI
from db import db
from models import WeatherForecast
from meteoblue_api import get_weather_data
from dotenv import load_dotenv
from sqlalchemy import inspect
import json
import io
import base64
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

from config import SQLALCHEMY_DATABASE_URI, METEOBLUE_API_KEY

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

@app.before_request
def create_tables():
    # Usando o 'inspect' da SQLAlchemy para verificar se a tabela existe
    if not inspect(db.engine).has_table("weather_forecast"):
        db.create_all()  # Cria as tabelas se não existirem

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/fetch_weather", methods=["POST"])
def fetch_weather():
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    city = "Unknown"

    # Obter os dados do clima
    weather_data = get_weather_data(latitude, longitude)

    if not weather_data:
        return jsonify({"error": "Failed to fetch data"}), 500

    # Função auxiliar para mapear pictocode para descrição textual
    def get_weather_description(code):
        mapping = {
            1: "Ensolarado",
            2: "Parcialmente nublado",
            3: "Nublado",
            5: "Nevoeiro",
            7: "Chuva leve",
            10: "Chuva forte",
            16: "Trovoadas",
            # Adicione outros códigos conforme necessário
        }
        return mapping.get(code, "Desconhecido")

    data = weather_data["data_day"]
    pictocodes = data.get("pictocode", [0] * len(data["time"]))
    description_list = [get_weather_description(code) for code in pictocodes]
    wind_speed_list = data.get("windspeed_mean", [0] * len(data["time"]))
    wind_direction_list = data.get("winddirection", ["N/A"] * len(data["time"]))
    precipitation_list = data.get("precipitation_probability", [0] * len(data["time"]))

    for i in range(len(data["time"])):
        time_value = data["time"][i]
        
        if isinstance(time_value, str):
            forecast_date = datetime.strptime(time_value, '%Y-%m-%d')
        else:
            forecast_date = datetime.utcfromtimestamp(time_value)
        
        forecast_date = forecast_date.strftime('%Y-%m-%d')

        forecast = WeatherForecast(
            forecast_date=forecast_date,
            temperature_min=data["temperature_min"][i],
            temperature_max=data["temperature_max"][i],
            weather_description=description_list[i],
            wind_speed=wind_speed_list[i],
            wind_direction=wind_direction_list[i],
            precipitation_probability=precipitation_list[i],
            city=city
        )
        db.session.add(forecast)

    db.session.commit()
    return render_template('index.html', success=True)



@app.route("/report", methods=["GET"])
def get_report():
    # Buscar as previsões no banco de dados
    forecasts = WeatherForecast.query.order_by(WeatherForecast.forecast_date).all()
    
    # Preparar dados para o gráfico
    dates = [f.forecast_date for f in forecasts]  # Agora 'forecast_date' já é do tipo Date
    min_temps = [f.temperature_min for f in forecasts]
    max_temps = [f.temperature_max for f in forecasts]
    wind_speeds = [f.wind_speed for f in forecasts]
    precipitation = [f.precipitation_probability for f in forecasts]

    # Gerar gráfico com Matplotlib (gráfico estático)
    plt.figure(figsize=(10, 5))
    plt.plot(dates, min_temps, label='Temperatura Mínima', color='blue')
    plt.plot(dates, max_temps, label='Temperatura Máxima', color='red')
    plt.xlabel('Data')
    plt.ylabel('Temperatura (°C)')
    plt.title('Previsão de Temperatura')
    plt.xticks(rotation=45)
    plt.legend()

    # Salvar o gráfico em base64 para renderização no frontend
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_data = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    # Gerar gráfico interativo com Plotly (gráfico dinâmico)
    fig = px.line(x=dates, y=[min_temps, max_temps], labels={'x': 'Data', 'y': 'Temperatura (°C)'},
                  title="Previsão de Temperatura")
    plotly_graph = fig.to_html(full_html=False)

    # Preparar o relatório em formato JSON para a resposta da API
    result = [{
        "date": f.forecast_date.strftime("%Y-%m-%d"),
        "min_temp": f.temperature_min,
        "max_temp": f.temperature_max,
        "description": f.weather_description,
        "wind_speed": f.wind_speed,
        "wind_direction": f.wind_direction,
        "precipitation_probability": f.precipitation_probability,
        "city": f.city
    } for f in forecasts]

    # Renderizar o template com dados e gráficos
    return render_template('index.html', result=result, img_data=img_data, plotly_graph=plotly_graph)

if __name__ == "__main__":
    app.run(debug=True)
