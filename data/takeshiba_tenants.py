"""竹芝ポートシティのテナント情報"""

TAKESHIBA_TENANTS = {
    "restaurants": [
        {
            "name": "レストラン・ボンマルシェ",
            "category": "フレンチ",
            "floor": "2F",
            "weather_preference": ["sunny", "cloudy"],
            "description": "本格フレンチレストラン。晴れの日のランチがおすすめ"
        },
        {
            "name": "和食処 海鮮",
            "category": "和食",
            "floor": "1F", 
            "weather_preference": ["rainy", "cloudy"],
            "description": "新鮮な海鮮料理。雨の日でも快適に過ごせる"
        },
        {
            "name": "カフェ・オーシャンビュー",
            "category": "カフェ",
            "floor": "3F",
            "weather_preference": ["sunny"],
            "description": "海を眺めながらコーヒーを楽しめる。晴れの日は絶景"
        },
        {
            "name": "ラーメン横丁",
            "category": "ラーメン", 
            "floor": "B1F",
            "weather_preference": ["rainy", "cold"],
            "description": "雨の日や寒い日に温まるラーメン店"
        }
    ],
    "shops": [
        {
            "name": "ファッションプラザ",
            "category": "アパレル",
            "floor": "1F-2F",
            "weather_preference": ["rainy", "cloudy"],
            "description": "雨の日のショッピングに最適"
        },
        {
            "name": "スポーツショップ アクティブ",
            "category": "スポーツ用品",
            "floor": "3F",
            "weather_preference": ["sunny"],
            "description": "アウトドア用品も充実。晴れの日の外出準備に"
        },
        {
            "name": "本とカフェの店",
            "category": "書店・カフェ",
            "floor": "2F",
            "weather_preference": ["rainy", "cloudy"],
            "description": "雨の日はゆっくり読書を楽しめる"
        }
    ],
    "entertainment": [
        {
            "name": "シネマコンプレックス",
            "category": "映画館",
            "floor": "4F",
            "weather_preference": ["rainy", "cloudy"],
            "description": "雨の日の定番エンターテイメント"
        },
        {
            "name": "ゲームセンター",
            "category": "アミューズメント",
            "floor": "3F",
            "weather_preference": ["rainy", "cloudy"],
            "description": "天気に関係なく楽しめる"
        },
        {
            "name": "展望デッキ",
            "category": "観光",
            "floor": "屋上",
            "weather_preference": ["sunny", "clear"],
            "description": "晴れの日は東京湾の絶景を楽しめる"
        }
    ]
}