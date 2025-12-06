from pathlib import Path
import urllib.request
import json

class OpenMeteoAPI:
    def __init__(self, location='RoundRock', days=7):
        self.lat = None
        self.lon = None
        self.location = location
        self.days = days
        self.daily_forecast = []
        self.hourly_forecast = []
        self.output_dir = './data/outputs/'

    def get_coordinates(self):
        # Step 1: Geocode to get lat/lon (supports city or postal code)
        geocode_url = f'https://geocoding-api.open-meteo.com/v1/search?name={self.location}&count=1&language=en&format=json'
        try:
            with urllib.request.urlopen(geocode_url) as response:
                geo_data = json.loads(response.read().decode())
                if not geo_data.get('results'):
                    raise ValueError("Location Not Found")
                lat = geo_data['results'][0]['latitude']
                lon = geo_data['results'][0]['longitude']
                print(f"Lat: {lat}\nLon: {lon}")
                self.lat = lat
                self.lon = lon
                self.geo_data = geo_data
        except Exception as e:
            print(f"Error geocoding: {e}")
            return None

    def get_openmeteo_daily_forecast(self):
        forecast_url = f'https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto&forecast_days={self.days}&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'
        try:
            with urllib.request.urlopen(forecast_url) as response:
                data = json.loads(response.read().decode())
                # Daily data: dates in 'daily.time', values in parallel lists (e.g., 'daily.temperature_2m_max')
                daily = data['daily']
                forecasts = [
                    {
                        'data':daily['time'][i],
                        'temp_max':daily['temperature_2m_max'][i],
                        'temp_min':daily['temperature_2m_min'][i],
                        'precipitation':daily['precipitation_sum'][i]
                    }
                    for i in range(len(daily['time']))
                ]
                self.daily_forecast = {'location': self.geo_data['results'][0]['name'], 'forecast': forecasts}
                return {'location': self.geo_data['results'][0]['name'], 'forecast': forecasts}
        except Exception as e:
            print(f"Error querying Open-Meteo: {e}")
            return None

    def get_openmeteo_hourly_forecast(self):
        hourly_params = [
            'temperature_2m',
            'precipitation',
            'cloud_cover',
            'wind_speed_10m',
            'wind_gusts_10m',
            'precipitation_probability',
            'weather_code',
            'visibility',
            'shortwave_radiation'
        ]

        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={self.lat}"
            f"&longitude={self.lon}"
            f"&forecast_days=1"
            f"&hourly={','.join(hourly_params)}"
            f"&timezone=auto"
            f"&temperature_unit=fahrenheit"
            f"&windspeed_unit=mph"
            f"&precipitation_unit=inch"
        )
        # hourly_forecast_today_url = f'https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&forecast_days=1&hourly=temperature_2m,precipitation,cloud_cover,wind_speed_10m,wind_gusts_10m,precipitation_probability,weather_code,visibility,shortwave_radiation&timezone=auto&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                hourly = data['hourly']
                hourly_forecasts = [
                    {
                        'data':hourly['time'][i],
                        'temp':hourly['temperature_2m'][i],
                        'precipitation':hourly['precipitation_probability'][i],
                        'cloud_cover':hourly['cloud_cover'][i],
                        'wind_speed':hourly['wind_speed_10m'][i],
                        'wind_gusts':hourly['wind_gusts_10m'][i],
                        'precipitation_probability':hourly['precipitation_probability'][i],
                        'weather_code':hourly['weather_code'][i],
                        'visibility':hourly['visibility'][i],
                    }
                    for i in range(len(hourly['time']))
                ]

                location_name = self.geo_data["results"][0]["name"]
                country = self.geo_data["results"][0].get("country", "")
                full_location = f"{location_name}, {country}" if country else location_name
                self.hourly_forecast = {'location':full_location, 'forecast': hourly_forecasts}
                return self.hourly_forecast
            
        except Exception as e:
            print(f"Error querying Open-Meteo: {e}")
            if hasattr(e, 'read'):
                print("Response Body: ", e.read().decode())
            return None
        
    def write_forecast(self):
        with open(Path(self.output_dir+'daily_forecast.json'), 'w') as f:
            json.dump(self.daily_forecast, f, indent=4)
        with open(Path(self.output_dir+'hourly_forecast.json'), 'w') as f:
            json.dump(self.hourly_forecast, f, indent=4)

def main():
    api = OpenMeteoAPI(location = "RoundRock", days=3)
    api.get_coordinates()
    daily_forecast = api.get_openmeteo_daily_forecast()
    # print(daily_forecast)
    hourly_forecast = api.get_openmeteo_hourly_forecast()
    # print(hourly_forecast)
    api.write_forecast()

if __name__ == "__main__":
    main()