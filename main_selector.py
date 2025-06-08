"""Selector方式 - 竹芝ポートシティマルチエージェントレコメンドシステム"""

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

class TakeshibaSelectorSystem:
    def __init__(self):
        self.setup_agents()
        self.weather_info = None
        self.user_request = None
    
    def setup_agents(self):
        """Selector方式用エージェントをセットアップ"""
        
        # ユーザープロキシエージェント
        self.user_proxy = autogen.UserProxyAgent(
            name="ユーザー代理",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config=False,
        )
        
        # 天気コンサルタント（天気関連の質問に特化）
        self.weather_consultant = autogen.AssistantAgent(
            name="天気コンサルタント",
            llm_config=llm_config,
            system_message="""
                あなたは天気に関する専門コンサルタントです。
                天気に関連する質問や、天候を考慮した活動提案が必要な時に発言してください。

                専門領域:
                - 現在の天気分析
                - 天候に適した活動スタイルの提案
                - 屋内外活動の判断
                - 季節やTPOに応じた服装アドバイス

                発言タイミング:
                - 天気情報の分析が必要な時
                - 天候を考慮した提案が求められる時
                - 他のエージェントが天気について質問した時
            """
        )
        
        # グルメ・カフェ専門家（食事関連に特化）
        self.gourmet_specialist = autogen.AssistantAgent(
            name="グルメ・カフェ専門家",
            llm_config=llm_config,
            system_message="""
                あなたはレストランとカフェの専門家です。
                食事、カフェ、グルメに関する要望がある時に発言してください。

                専門領域:
                - レストランの選び方
                - カフェでの過ごし方
                - 天気に適した食事スタイル
                - 時間帯に応じた食事提案

                発言タイミング:
                - 「ランチ」「ディナー」「カフェ」「食事」などの要望がある時
                - 他のエージェントが食事について相談した時
                - 天気に適した食事スタイルの提案が必要な時
            """
        )
        
        # ショッピングアドバイザー（買い物に特化）
        self.shopping_advisor = autogen.AssistantAgent(
            name="ショッピングアドバイザー",
            llm_config=llm_config,
            system_message="""
                あなたはショッピングの専門アドバイザーです。
                買い物、ファッション、雑貨に関する要望がある時に発言してください。

                専門領域:
                - ファッション・アパレル
                - 雑貨・ライフスタイル用品
                - お土産・ギフト選び
                - 効率的なショッピングルート

                発言タイミング:
                - 「ショッピング」「買い物」「服」「雑貨」などの要望がある時
                - 他のエージェントがショッピングについて相談した時
                - 天気に適したショッピングスタイルの提案が必要な時
            """
        )
        
        # エンターテイメントプロデューサー（娯楽に特化）
        self.entertainment_producer = autogen.AssistantAgent(
            name="エンターテイメントプロデューサー",
            llm_config=llm_config,
            system_message="""
                あなたはエンターテイメントのプロデューサーです。
                娯楽、映画、ゲーム、体験に関する要望がある時に発言してください。

                専門領域:
                - 映画・シアター
                - ゲーム・アミューズメント
                - 体験型アクティビティ
                - イベント・ワークショップ

                発言タイミング:
                - 「映画」「ゲーム」「エンターテイメント」「体験」などの要望がある時
                - 他のエージェントが娯楽について相談した時
                - 天気に適したエンターテイメントの提案が必要な時
            """
        )
        
        # ライフスタイルコンシェルジュ（総合サービス）
        self.lifestyle_concierge = autogen.AssistantAgent(
            name="ライフスタイルコンシェルジュ",
            llm_config=llm_config,
            system_message="""
                あなたは総合的なライフスタイルコンシェルジュです。
                複数分野にまたがる相談や、最終的な統合提案が必要な時に発言してください。

                専門領域:
                - 複合的な提案の統合
                - 時間配分とスケジューリング
                - 代替案の提示
                - 実用的なアドバイス

                発言タイミング:
                - 複数分野の統合が必要な時
                - 最終的なまとめが求められる時
                - 他のエージェントの提案を組み合わせる時
                - 議論をまとめて終了する時（TERMINATE付きで）
            """
        )
        
        # リラクゼーション専門家（リラックス・休憩に特化）
        self.relaxation_expert = autogen.AssistantAgent(
            name="リラクゼーション専門家",
            llm_config=llm_config,
            system_message="""
                あなたはリラクゼーションとくつろぎの専門家です。
                休憩、リラックス、ゆっくり過ごすことに関する要望がある時に発言してください。

                専門領域:
                - 癒しとリラクゼーション
                - 静かな過ごし方
                - 美容・健康サービス
                - のんびりとした時間の使い方

                発言タイミング:
                - 「リラックス」「ゆっくり」「休憩」「癒し」などの要望がある時
                - ストレス解消や疲労回復についての相談がある時
                - 静かで落ち着いた過ごし方の提案が必要な時
            """
        )

    def get_weather_info(self):
        """現在の天気情報を取得"""
        return weather_service.get_current_weather()

    def get_user_request(self):
        """ユーザーからの要望を取得"""
        print("""
            === Selector方式 - 竹芝ポートシティ レコメンドシステム ===

            AIが文脈に応じて最適な専門家を自動選択します。
            利用可能な専門家:
            - 天気コンサルタント (天候分析)
            - グルメ・カフェ専門家 (食事・カフェ)
            - ショッピングアドバイザー (買い物)
            - エンターテイメントプロデューサー (娯楽)
            - リラクゼーション専門家 (休憩・癒し)
            - ライフスタイルコンシェルジュ (総合統合)

            今日はどのようなことをお手伝いできますか？
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

    def start_selector_discussion(self):
        """Selector方式でマルチエージェント議論を開始"""
        
        # 1. 天気情報取得
        self.weather_info = self.get_weather_info()
        
        # 2. ユーザー要望取得
        self.user_request = self.get_user_request()
        
        print("\n" + "="*60)
        print("Selector方式エージェント会議を開始します...")
        print("AIが文脈に応じて最適な専門家を自動選択します")
        print("="*60)
        
        # 3. 基本情報をまとめる
        base_context = f"""
            【Selector方式会議】竹芝ポートシティでのおすすめ提案

            【現在の天気情報】
            - 天気: {self.weather_info['description']}
            - 気温: {self.weather_info['temperature']}°C
            - 湿度: {self.weather_info['humidity']}%

            【ユーザーからの要望】
            {self.user_request}

            【利用可能なテナント情報】
            {self.format_tenant_data()}

            ===== Selector議論開始 =====
            ユーザーの要望と文脈に応じて、最適な専門家が自動選択されます。
            関連する専門家が議論し、最終的にライフスタイルコンシェルジュがまとめます。
        """
                    
        # 4. Selector形式のグループチャット
        agents = [
            self.weather_consultant,
            self.gourmet_specialist,
            self.shopping_advisor,
            self.entertainment_producer,
            self.relaxation_expert,
            self.lifestyle_concierge
        ]
        
        # Selector設定（AutoGenがコンテキストに基づいて選択）
        groupchat = autogen.GroupChat(
            agents=agents,
            messages=[],
            max_round=8,  # 十分な議論回数
            speaker_selection_method="auto"  # AIが自動選択
        )
        
        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config=llm_config,
            system_message="""
                あなたはSelector方式の会議進行管理者です。
                ユーザーの要望と議論の文脈に応じて、最も適切な専門家を選択してください。

                選択基準:
                - ユーザーの要望に最も関連する専門分野
                - 現在の議論の流れに適した専門家
                - 天気情報を考慮した最適な提案者
                - 最終的な統合にはライフスタイルコンシェルジュを選択

                効率的で価値ある議論となるよう、適切なエージェント選択を行ってください。
            """
        )
        
        # 会議開始
        self.user_proxy.initiate_chat(
            manager,
            message=base_context,
            clear_history=True
        )
        
        print("\n" + "="*60)
        print("Selector方式会議が終了しました。")
        print("="*60)

def main():
    """メイン関数"""
    print("竹芝ポートシティ Selector マルチエージェントシステムを開始します...")
    
    try:
        # システム初期化
        recommendation_system = TakeshibaSelectorSystem()
        
        # Selector議論開始
        recommendation_system.start_selector_discussion()
        
    except KeyboardInterrupt:
        print("\n\nシステムを終了します。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    main()