"""Round Robin方式 - 竹芝ポートシティマルチエージェントレコメンドシステム"""

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

class TakeshibaRoundRobinSystem:
    def __init__(self):
        self.setup_agents()
        self.weather_info = None
        self.user_request = None
    
    def setup_agents(self):
        """Round Robin方式用エージェントをセットアップ"""
        
        # ユーザープロキシエージェント（司会者）
        self.user_proxy = autogen.UserProxyAgent(
            name="司会者",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config=False,
        )
        
        # 1. 天気分析エージェント（最初に発言）
        self.weather_agent = autogen.AssistantAgent(
            name="天気分析エージェント",
            llm_config=llm_config,
            system_message="""
                あなたは会議の最初に発言する天気分析の専門家です。
                現在の天気情報を分析し、今日の外出に適した活動スタイルを提案してください。

                発言順序: 1番目（会議開始）
                役割: 天気に基づく基本的な活動指針を設定
                - 屋内/屋外活動の適性
                - 服装や持ち物のアドバイス
                - 時間帯による天気変化の考慮

                次のエージェントのために、天気を踏まえた活動の方向性を明確に示してください。
            """
        )
        
        # 2. 施設情報エージェント（2番目に発言）
        self.facility_agent = autogen.AssistantAgent(
            name="施設情報エージェント",
            llm_config=llm_config,
            system_message="""
                あなたは2番目に発言する施設情報の専門家です。
                天気分析エージェントの提案を受けて、竹芝ポートシティの利用可能な施設を整理してください。

                発言順序: 2番目
                役割: 利用可能な選択肢の整理
                - 各フロアの施設配置
                - 天気に適した施設の抽出
                - 営業時間や特徴の整理

                次の専門エージェントが具体的な提案をしやすいよう、施設の基本情報を整理してください。
            """
        )
        
        # 3. ショッピング専門エージェント（3番目に発言）
        self.shopping_agent = autogen.AssistantAgent(
            name="ショッピング専門エージェント",
            llm_config=llm_config,
            system_message="""
                あなたは3番目に発言するショッピングの専門家です。
                天気と施設情報を踏まえ、お買い物の観点から具体的な提案をしてください。

                発言順序: 3番目
                役割: ショッピング体験の具体化
                - 天気に適したショッピングスタイル
                - おすすめ商品カテゴリ
                - お店の回り方や時間配分

                ユーザーの要望に応じて、ショッピングプランを提案してください。
            """
        )
        
        # 4. エンターテイメント専門エージェント（4番目に発言）
        self.entertainment_agent = autogen.AssistantAgent(
            name="エンターテイメント専門エージェント",
            llm_config=llm_config,
            system_message="""
                あなたは4番目に発言するエンターテイメントの専門家です。
                これまでの議論を踏まえ、楽しい時間の過ごし方を提案してください。

                発言順序: 4番目
                役割: エンターテイメント要素の追加
                - 天気に適した娯楽活動
                - 時間帯に応じたアクティビティ
                - ショッピングとの組み合わせ

                前のエージェントの提案を補完する形で、総合的な楽しみ方を提案してください。
            """
        )
        
        # 5. 総合コーディネーター（最後に発言）
        self.coordinator_agent = autogen.AssistantAgent(
            name="総合コーディネーター",
            llm_config=llm_config,
            system_message="""
                あなたは最後に発言する総合コーディネーターです。
                全てのエージェントの意見を統合し、実行可能な1日プランを作成してください。

                発言順序: 5番目（最終発言）
                役割: 統合と最終提案
                - 各専門家の意見を整理統合
                - 時系列での行動プラン作成
                - 代替案の提示
                - 実用的なアドバイスの追加

                最終的に、ユーザーが実行しやすい具体的なプランを提示してください。
                必ず発言の最後に「TERMINATE」を付けて会議を終了してください。
            """
        )

    def get_weather_info(self):
        """現在の天気情報を取得"""
        return weather_service.get_current_weather()

    def get_user_request(self):
        """ユーザーからの要望を取得"""
        print("""
            === Round Robin方式 - 竹芝ポートシティ レコメンドシステム ===

            順番に各専門家が発言し、段階的に提案を構築します。
            発言順序: 天気分析 → 施設情報 → ショッピング → エンタメ → 総合コーディネート

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

    def start_round_robin_discussion(self):
        """Round Robin方式でマルチエージェント議論を開始"""
        
        # 1. 天気情報取得
        self.weather_info = self.get_weather_info()
        
        # 2. ユーザー要望取得
        self.user_request = self.get_user_request()
        
        print("\n" + "="*60)
        print("Round Robin方式エージェント会議を開始します...")
        print("発言順序: 天気→施設→ショッピング→エンタメ→総合")
        print("="*60)
        
        # 3. 基本情報をまとめる
        base_context = f"""
            【Round Robin会議】竹芝ポートシティでのおすすめ提案

            【現在の天気情報】
            - 天気: {self.weather_info['description']}
            - 気温: {self.weather_info['temperature']}°C
            - 湿度: {self.weather_info['humidity']}%

            【ユーザーからの要望】
            {self.user_request}

            【利用可能なテナント情報】
            {self.format_tenant_data()}

            ===== Round Robin議論開始 =====
            各エージェントは順番に発言してください。前のエージェントの発言を受けて、
            段階的に提案を発展させてください。
        """
        
        # 4. Round Robin形式のグループチャット
        agents = [
            self.weather_agent,
            self.facility_agent, 
            self.shopping_agent,
            self.entertainment_agent,
            self.coordinator_agent
        ]
        
        # Round Robin設定
        groupchat = autogen.GroupChat(
            agents=agents,
            messages=[],
            max_round=6,  # 各エージェント1回ずつ + 余裕
            speaker_selection_method="round_robin"  # 明示的にRound Robin指定
        )
        
        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config=llm_config,
            system_message="""
                あなたはRound Robin形式の会議進行管理者です。
                エージェントが順番に発言し、段階的に提案を構築するよう進行してください。
                各エージェントは前の発言を踏まえて、自分の専門分野から貢献してください。
            """
        )
        
        # 会議開始
        self.user_proxy.initiate_chat(
            manager,
            message=base_context,
            clear_history=True
        )
        
        print("\n" + "="*60)
        print("Round Robin会議が終了しました。")
        print("="*60)

def main():
    """メイン関数"""
    print("竹芝ポートシティ Round Robin マルチエージェントシステムを開始します...")
    
    try:
        # システム初期化
        recommendation_system = TakeshibaRoundRobinSystem()
        
        # Round Robin議論開始
        recommendation_system.start_round_robin_discussion()
        
    except KeyboardInterrupt:
        print("\n\nシステムを終了します。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    main()