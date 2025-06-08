"""AutoGenを使った竹芝ポートシティマルチエージェントレコメンドシステム"""

import os
import autogen
from dotenv import load_dotenv
from data.takeshiba_tenants import TAKESHIBA_TENANTS
from utils.weather_service import WeatherService

# 環境変数を読み込み
load_dotenv()

# LLM設定
config_list = [
    {
        "model": "gpt-4o",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.7,
}

# 天気サービス初期化
weather_service = WeatherService()

class TakeshibaMultiAgentSystem:
    def __init__(self):
        self.setup_agents()
        self.weather_info = None
        self.user_request = None
    
    def setup_agents(self):
        """エージェントをセットアップ"""
        
        # ユーザープロキシエージェント（司会者）
        self.user_proxy = autogen.UserProxyAgent(
            name="司会者",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config=False,
            system_message="""
                あなたは竹芝ポートシティのレコメンド会議の司会者です。
                各専門エージェントからの情報を整理し、最終的な推薦をユーザーに提供します。
            """
        )
        
        # 天気情報エージェント
        self.weather_agent = autogen.AssistantAgent(
            name="天気エージェント",
            llm_config=llm_config,
            system_message="""
                あなたは天気情報の専門エージェントです。
                現在の天気情報を分析し、その天気に適した活動やお出かけスタイルを提案します。
                - 晴れ：屋外活動、テラス席、散歩に適している
                - 雨：屋内活動、カフェでのんびり、ショッピングに適している  
                - 曇り：どんな活動でも快適
                - 暑い日：涼しい屋内、冷たい飲み物がおすすめ
                - 寒い日：暖かい屋内、温かい飲み物がおすすめ

                天気の状況を踏まえた活動アドバイスを簡潔に提供してください。
            """
        )
                        
        # テナント情報エージェント
        self.tenant_agent = autogen.AssistantAgent(
            name="テナント情報エージェント",
            llm_config=llm_config,
            system_message="""
                あなたは竹芝ポートシティのテナント情報専門エージェントです。
                利用可能な店舗やサービスの詳細情報を正確に提供します。
                - 各テナントの場所（階数）
                - 営業時間や特徴
                - 天気との相性
                - カテゴリ別の分類

                テナント情報は正確で実用的な情報を提供し、ユーザーの要望と天気を考慮して適切な選択肢を提示してください。
            """
        )
        
        # ショッピング専門エージェント
        self.shopping_agent = autogen.AssistantAgent(
            name="ショッピング専門エージェント",
            llm_config=llm_config,
            system_message="""
                あなたはショッピングの専門エージェントです。
                竹芝ポートシティでのお買い物体験を最大化するための提案を行います。

                専門分野：
                - ファッション・アパレル
                - 雑貨・ライフスタイル用品
                - お土産・ギフト
                - 季節商品・トレンドアイテム

                天気や季節を考慮して、今日のお買い物に最適な商品やお店の組み合わせを提案します。
                実用的で楽しいショッピング体験を演出してください。
            """
        )
        
        # エンターテイメント専門エージェント  
        self.entertainment_agent = autogen.AssistantAgent(
            name="エンターテイメント専門エージェント",
            llm_config=llm_config,
            system_message="""
                あなたはエンターテイメントの専門エージェントです。
                竹芝ポートシティでの楽しい時間の過ごし方を提案します。

                専門分野：
                - 映画・シアター
                - ゲーム・アミューズメント
                - 体験型アクティビティ
                - イベント・ワークショップ
                - カラオケ・パーティー

                天気や時間帯を考慮して、今日にぴったりのエンターテイメント体験を提案します。
                ワクワクする楽しい提案を心がけてください。
            """
        )
        
        # 総合レコメンドエージェント
        self.recommend_agent = autogen.AssistantAgent(
            name="総合レコメンドエージェント",
            llm_config=llm_config,
            system_message="""
                あなたは総合レコメンドの専門エージェントです。
                他のエージェントからの情報を統合し、ユーザーに最適化された提案を行います。

                役割：
                - 各専門エージェントの意見を整理統合
                - ユーザーの要望と天気情報のバランス調整
                - 実行可能で楽しい1日のプランを提案
                - 代替案も含めた柔軟な提案

                最終的に、具体的で実行しやすい推薦プランを日本語で親しみやすく提示してください。
            """
        )

    def get_weather_info(self):
        """現在の天気情報を取得"""
        return weather_service.get_current_weather()

    def get_user_request(self):
        """ユーザーからの要望を取得"""
        print("""
            === 竹芝ポートシティ マルチエージェント レコメンドシステム ===

            こんにちは！今日はどのようなことをお手伝いできますか？
            例：
            - 「美味しいランチを食べたい」
            - 「雨の日でも楽しめる場所を探している」
            - 「ショッピングを楽しみたい」
            - 「映画やエンターテイメントに興味がある」
            - 「カフェでゆっくりしたい」
        """)
        
        # デモモード用の環境変数チェック
        demo_request = os.getenv("DEMO_REQUEST")
        if demo_request:
            print(f"\n[デモモード] ユーザー要望: {demo_request}")
            return demo_request
        
        user_input = input("\nあなたのご要望をお聞かせください: ")
        return user_input

    def format_tenant_data(self):
        """テナントデータをエージェント用にフォーマット"""
        formatted_data = "=== 竹芝ポートシティ テナント情報 ===\n\n"
        
        for category, tenants in TAKESHIBA_TENANTS.items():
            formatted_data += f"【{category}】\n"
            for tenant in tenants:
                weather_pref = tenant.get("weather_preference", [])
                weather_info = f" (適した天気: {', '.join(weather_pref)})" if weather_pref else ""
                formatted_data += f"- {tenant['name']} ({tenant['floor']}){weather_info}\n"
                formatted_data += f"  {tenant['description']}\n"
            formatted_data += "\n"
        
        return formatted_data

    def start_multi_agent_discussion(self):
        """マルチエージェント議論を開始"""
        
        # 1. 天気情報取得
        self.weather_info = self.get_weather_info()
        
        # 2. ユーザー要望取得
        self.user_request = self.get_user_request()
        
        print("\n" + "="*50)
        print("エージェント会議を開始します...")
        print("="*50)
        
        # 3. 基本情報をまとめる
        base_context = f"""
            【会議テーマ】竹芝ポートシティでのおすすめ提案

            【現在の天気情報】
            - 天気: {self.weather_info['description']}
            - 気温: {self.weather_info['temperature']}°C
            - 湿度: {self.weather_info['humidity']}%

            【ユーザーからの要望】
            {self.user_request}

            【利用可能なテナント情報】
            {self.format_tenant_data()}

            上記の情報を基に、各専門分野の観点から提案をお願いします。
        """
        
        # 4. グループチャットでマルチエージェント議論
        agents = [
            self.weather_agent,
            self.tenant_agent, 
            self.shopping_agent,
            self.entertainment_agent,
            self.recommend_agent
        ]
        
        # グループチャット設定
        groupchat = autogen.GroupChat(
            agents=agents,
            messages=[],
            max_round=10,
            speaker_selection_method="round_robin"
        )
        
        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config=llm_config,
            system_message="""
                あなたは竹芝ポートシティレコメンド会議の進行管理者です。
                各エージェントが順番に発言し、最終的に総合レコメンドエージェントがまとめを行うよう進行してください。
                会議は効率的に進め、ユーザーにとって価値ある提案となるよう調整してください。
            """
        )
        
        # 会議開始
        self.user_proxy.initiate_chat(
            manager,
            message=base_context,
            clear_history=True
        )
        
        print("\n" + "="*50)
        print("会議が終了しました。ありがとうございました！")
        print("="*50)

def main():
    """メイン関数"""
    print("竹芝ポートシティ マルチエージェント レコメンドシステムを開始します...")
    
    try:
        # システム初期化
        recommendation_system = TakeshibaMultiAgentSystem()
        
        # マルチエージェント議論開始
        recommendation_system.start_multi_agent_discussion()
        
    except KeyboardInterrupt:
        print("\n\nシステムを終了します。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    main()