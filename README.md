# 竹芝ポートシティ レコメンドシステム

AutoGenライブラリを使用したマルチエージェントシステムで、現在の天気情報を考慮して竹芝ポートシティのテナントをおすすめします。

## 機能

- 現在の天気情報の取得
- 天気に応じたテナント推薦
- マルチエージェントによる対話式レコメンド
- Code Interpreter機能（Docker環境）

## セットアップ

1. 環境変数の設定:
```bash
cp .env.example .env
# .envファイルを編集してAPIキーを設定
```

2. Docker環境での起動:
```bash
docker-compose up --build
```

## 必要なAPIキー

- OpenAI API Key: GPT-4モデル使用のため
- Weather API Key: OpenWeatherMap API（オプション）

## エージェント構成

- **Weather Agent**: 天気情報の取得と分析
- **Tenant Agent**: 竹芝ポートシティのテナント情報管理  
- **Recommend Agent**: 天気とテナント情報を組み合わせた推薦
- **User Proxy**: ユーザーとの対話インターフェース