from db import db
from datetime import datetime

class WeatherForecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forecast_date = db.Column(db.Date, nullable=False)
    temperature_min = db.Column(db.Float)
    temperature_max = db.Column(db.Float)
    weather_description = db.Column(db.Text)
    wind_speed = db.Column(db.Float)
    wind_direction = db.Column(db.String(10))
    precipitation_probability = db.Column(db.Float)
    city = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, forecast_date, temperature_min, temperature_max, weather_description,
                 wind_speed, wind_direction, precipitation_probability, city):
        # Garantindo que a forecast_date seja convertida para o tipo datetime.date
        if isinstance(forecast_date, str):
            forecast_date = datetime.strptime(forecast_date, '%Y-%m-%d').date()
        
        self.forecast_date = forecast_date
        self.temperature_min = temperature_min
        self.temperature_max = temperature_max
        self.weather_description = weather_description
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.precipitation_probability = precipitation_probability
        self.city = city
