from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from config import SQLALCHEMY_DATABASE_URI
from db import db
from models import WeatherForecast
from meteoblue_api import get_weather_data
from dotenv import load_dotenv
from sqlalchemy import inspect
import json
import io
import os
import base64
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

# Configurar o agendador
scheduler = BackgroundScheduler(daemon=True)

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
    }
    return mapping.get(code, "Desconhecido")

# Função para atualizar os dados automaticamente
def update_weather_data():
    latitude = "-23.55"
    longitude = "-46.63"

    weather_data = get_weather_data(latitude, longitude)

    if weather_data:
        data = weather_data["data_day"]
        pictocodes = data.get("pictocode", [0] * len(data["time"]))
        description_list = [get_weather_description(code) for code in pictocodes]
        wind_speed_list = data.get("windspeed_mean", [0] * len(data["time"]))
        wind_direction_list = data.get("winddirection", ["N/A"] * len(data["time"]))
        precipitation_list = data.get("precipitation_probability", [0] * len(data["time"]))

        for i in range(len(data["time"])):
            time_value = data["time"][i]
            forecast_date = datetime.strptime(time_value, '%Y-%m-%d').date()

            forecast = WeatherForecast(
                forecast_date=forecast_date,
                temperature_min=data["temperature_min"][i],
                temperature_max=data["temperature_max"][i],
                weather_description=description_list[i],
                wind_speed=wind_speed_list[i],
                wind_direction=wind_direction_list[i],
                precipitation_probability=precipitation_list[i],
                city="Unknown"
            )
            db.session.add(forecast)

        db.session.commit()

        # ✅ Salva a hora da última atualização
        with open("last_update.txt", "w") as f:
            f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Agendar a atualização automática a cada 6 horas
scheduler.add_job(update_weather_data, 'interval', hours=6)
scheduler.start()

@app.before_request
def create_tables():
    if not inspect(db.engine).has_table("weather_forecast"):
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/fetch_weather", methods=["POST"])
def fetch_weather():
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    data_inicial = request.form.get("data_inicial")
    data_final = request.form.get("data_final")

    city = "Unknown"
    weather_data = get_weather_data(latitude, longitude)

    if not weather_data:
        return jsonify({"error": "Failed to fetch data"}), 500

    data = weather_data["data_day"]
    pictocodes = data.get("pictocode", [0] * len(data["time"]))
    description_list = [get_weather_description(code) for code in pictocodes]
    wind_speed_list = data.get("windspeed_mean", [0] * len(data["time"]))
    wind_direction_list = data.get("winddirection", ["N/A"] * len(data["time"]))
    precipitation_list = data.get("precipitation_probability", [0] * len(data["time"]))

    data_ini = datetime.strptime(data_inicial, '%Y-%m-%d').date() if data_inicial else None
    data_fim = datetime.strptime(data_final, '%Y-%m-%d').date() if data_final else None

    for i in range(len(data["time"])):
        time_value = data["time"][i]
        forecast_date_obj = datetime.strptime(time_value, '%Y-%m-%d')
        forecast_date_only = forecast_date_obj.date()

        if data_ini and forecast_date_only < data_ini:
            continue
        if data_fim and forecast_date_only > data_fim:
            continue

        forecast = WeatherForecast(
            forecast_date=forecast_date_only,
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
    data_inicial = request.args.get('data_inicial')
    data_final = request.args.get('data_final')

    data_ini = datetime.strptime(data_inicial, '%Y-%m-%d').date() if data_inicial else None
    data_fim = datetime.strptime(data_final, '%Y-%m-%d').date() if data_final else None

    filters = []
    if data_ini:
        filters.append(WeatherForecast.forecast_date >= data_ini)
    if data_fim:
        filters.append(WeatherForecast.forecast_date <= data_fim)

    forecasts = WeatherForecast.query.filter(*filters).order_by(WeatherForecast.forecast_date).all()

    dates = [f.forecast_date for f in forecasts]
    min_temps = [f.temperature_min for f in forecasts]
    max_temps = [f.temperature_max for f in forecasts]
    wind_speeds = [f.wind_speed for f in forecasts]
    precipitation = [f.precipitation_probability for f in forecasts]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, min_temps, label='Temperatura Mínima', color='blue')
    plt.plot(dates, max_temps, label='Temperatura Máxima', color='red')
    plt.xlabel('Data')
    plt.ylabel('Temperatura (°C)')
    plt.title('Previsão de Temperatura')
    plt.xticks(rotation=45)
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_data = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    fig = px.line(x=dates, y=[min_temps, max_temps], labels={'x': 'Data', 'y': 'Temperatura (°C)'}, title="Previsão de Temperatura")
    plotly_graph = fig.to_html(full_html=False)

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

    # ✅ Lê a hora da última atualização automática
    last_update = None
    if os.path.exists("last_update.txt"):
        with open("last_update.txt", "r") as f:
            last_update = datetime.strptime(f.read().strip(), '%Y-%m-%d %H:%M:%S') \
                .strftime('%d/%m/%Y às %H:%M')

    return render_template(
        'index.html',
        result=result,
        img_data=img_data,
        plotly_graph=plotly_graph,
        last_update=last_update
    )

if __name__ == "__main__":
    app.run(debug=True)
