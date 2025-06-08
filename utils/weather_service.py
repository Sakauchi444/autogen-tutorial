"""天気情報取得サービス"""

import requests
import os
from typing import Dict, Optional

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_current_weather(self, city: str = "Tokyo") -> Optional[Dict]:
        """現在の天気情報を取得"""
        if not self.api_key:
            # APIキーがない場合のダミーデータ
            return {
                "weather": "sunny",
                "temperature": 22,
                "description": "晴れ",
                "humidity": 60
            }
        
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'ja'
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            weather_condition = self._classify_weather(data['weather'][0]['main'])
            
            return {
                "weather": weather_condition,
                "temperature": data['main']['temp'],
                "description": data['weather'][0]['description'],
                "humidity": data['main']['humidity']
            }
            
        except Exception as e:
            print(f"天気情報の取得に失敗しました: {e}")
            # フォールバック用のダミーデータ
            return {
                "weather": "cloudy",
                "temperature": 20,
                "description": "曇り",
                "humidity": 70
            }
    
    def _classify_weather(self, weather_main: str) -> str:
        """天気情報を分類"""
        weather_map = {
            'Clear': 'sunny',
            'Clouds': 'cloudy', 
            'Rain': 'rainy',
            'Drizzle': 'rainy',
            'Thunderstorm': 'rainy',
            'Snow': 'cold',
            'Mist': 'cloudy',
            'Fog': 'cloudy'
        }
        
        return weather_map.get(weather_main, 'cloudy')