"""Swarm方式 - 竹芝ポートシティマルチエージェントレコメンドシステム"""

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

class TakeshibaSwarmSystem:
    def __init__(self):
        self.setup_agents()
        self.weather_info = None
        self.user_request = None
    
    def setup_agents(self):
        """Swarm方式用エージェントをセットアップ"""
        
        # ユーザープロキシエージェント
        self.user_proxy = autogen.UserProxyAgent(
            name="コーディネーター",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config=False,
        )
        
        # Swarm Agent 1: アクティブ体験リサーチャー
        self.active_researcher = autogen.AssistantAgent(
            name="アクティブ体験リサーチャー",
            llm_config=llm_config,
            system_message="""
                あなたはアクティブな体験を重視するリサーチャーです。
                Swarm方式で他のエージェントと並行して、独自の視点から提案を作成してください。

                あなたの視点:
                - エネルギッシュで活動的な過ごし方
                - 体験型・参加型のアクティビティ
                - 新しい発見や刺激的な体験
                - 身体を動かす要素を含む提案

                Swarmアプローチ:
                - 他のエージェントとは独立して分析
                - 自分独自の結論を導き出す
                - 最終的に他の提案と比較検討される
                - アクティブ志向の具体的プランを提示

                ユーザーの要望に対して、アクティブ体験の観点から竹芝ポートシティでの過ごし方を提案してください。
            """
        )
        
        # Swarm Agent 2: リラクゼーション・キュレーター
        self.relaxation_curator = autogen.AssistantAgent(
            name="リラクゼーション・キュレーター",
            llm_config=llm_config,
            system_message="""
                あなたはリラックスと癒しを重視するキュレーターです。
                Swarm方式で他のエージェントと並行して、独自の視点から提案を作成してください。

                あなたの視点:
                - 心身のリラクゼーション
                - ゆったりとした時間の過ごし方
                - 癒しと安らぎの体験
                - ストレス解消と心の平穏

                Swarmアプローチ:
                - 他のエージェントとは独立して分析
                - リラクゼーション特化の結論を導き出す
                - 最終的に他の提案と比較検討される
                - 癒し志向の具体的プランを提示

                ユーザーの要望に対して、リラクゼーションの観点から竹芝ポートシティでの過ごし方を提案してください。
            """
        )
        
        # Swarm Agent 3: トレンド・イノベーター
        self.trend_innovator = autogen.AssistantAgent(
            name="トレンド・イノベーター",
            llm_config=llm_config,
            system_message="""
                あなたは最新トレンドと革新的な体験を重視するイノベーターです。
                Swarm方式で他のエージェントと並行して、独自の視点から提案を作成してください。

                あなたの視点:
                - 最新のトレンドとファッション
                - 革新的で斬新な体験
                - SNS映えする体験
                - 今話題のスポットや活動

                Swarmアプローチ:
                - 他のエージェントとは独立して分析
                - トレンド特化の結論を導き出す
                - 最終的に他の提案と比較検討される
                - イノベーション志向の具体的プランを提示

                ユーザーの要望に対して、最新トレンドの観点から竹芝ポートシティでの過ごし方を提案してください。
            """
        )
        
        # Swarm Agent 4: 実用性・エフィシエンシー専門家
        self.efficiency_expert = autogen.AssistantAgent(
            name="実用性・エフィシエンシー専門家",
            llm_config=llm_config,
            system_message="""
                あなたは実用性と効率性を重視する専門家です。
                Swarm方式で他のエージェントと並行して、独自の視点から提案を作成してください。

                あなたの視点:
                - 時間効率と移動効率
                - コストパフォーマンス
                - 実用的で現実的な提案
                - 無駄のないスマートな過ごし方

                Swarmアプローチ:
                - 他のエージェントとは独立して分析
                - 効率性特化の結論を導き出す
                - 最終的に他の提案と比較検討される
                - 実用性志向の具体的プランを提示

                ユーザーの要望に対して、実用性と効率性の観点から竹芝ポートシティでの過ごし方を提案してください。
            """
        )
        
        # Swarm Agent 5: 文化・グルメ探求者
        self.culture_gourmet_explorer = autogen.AssistantAgent(
            name="文化・グルメ探求者",
            llm_config=llm_config,
            system_message="""
                あなたは文化とグルメを重視する探求者です。
                Swarm方式で他のエージェントと並行して、独自の視点から提案を作成してください。

                あなたの視点:
                - 食文化とグルメ体験
                - 文化的価値のある体験
                - 味覚と感性を重視
                - 地域性や季節感を活かした提案

                Swarmアプローチ:
                - 他のエージェントとは独立して分析
                - 文化・グルメ特化の結論を導き出す
                - 最終的に他の提案と比較検討される
                - 文化・グルメ志向の具体的プランを提示

                ユーザーの要望に対して、文化とグルメの観点から竹芝ポートシティでの過ごし方を提案してください。
            """
        )
        
        # Swarm統合エージェント: マスター・シンセサイザー
        self.master_synthesizer = autogen.AssistantAgent(
            name="マスター・シンセサイザー",
            llm_config=llm_config,
            system_message="""
                あなたはSwarm方式の最終統合を行うマスター・シンセサイザーです。
                全てのSwarmエージェントの独立した提案を統合し、最適解を導き出してください。

                統合プロセス:
                1. 各Swarmエージェントの提案を分析
                2. それぞれの視点の価値を評価
                3. ユーザーの要望と天気情報に最適な組み合わせを選択
                4. 複数の視点を融合した総合プランを作成
                5. 代替案も含めた柔軟な提案

                最終提案の特徴:
                - 各専門分野の利点を活かした統合プラン
                - ユーザーの要望に最も適した優先順位
                - 実行可能で具体的な行動計画
                - 天気や状況に応じた柔軟性

                必ず最後に「TERMINATE」を付けて議論を終了してください。
            """
        )

    def get_weather_info(self):
        """現在の天気情報を取得"""
        return weather_service.get_current_weather()

    def get_user_request(self):
        """ユーザーからの要望を取得"""
        print("""
            === Swarm方式 - 竹芝ポートシティ レコメンドシステム ===

            複数のエージェントが並行して独立分析し、最終的に統合します。
            Swarmエージェント:
            - アクティブ体験リサーチャー (活動的・体験重視)
            - リラクゼーション・キュレーター (癒し・安らぎ重視)
            - トレンド・イノベーター (最新・革新重視)
            - 実用性・エフィシエンシー専門家 (効率・実用重視)
            - 文化・グルメ探求者 (文化・美食重視)

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

    def start_swarm_discussion(self):
        """Swarm方式でマルチエージェント議論を開始"""
        
        # 1. 天気情報取得
        self.weather_info = self.get_weather_info()
        
        # 2. ユーザー要望取得
        self.user_request = self.get_user_request()
        
        print("\n" + "="*60)
        print("Swarm方式エージェント会議を開始します...")
        print("複数エージェントが並行して独立分析し、最終統合を行います")
        print("="*60)
        
        # 3. 基本情報をまとめる
        base_context = f"""
            【Swarm方式会議】竹芝ポートシティでのおすすめ提案

            【現在の天気情報】
            - 天気: {self.weather_info['description']}
            - 気温: {self.weather_info['temperature']}°C
            - 湿度: {self.weather_info['humidity']}%

            【ユーザーからの要望】
            {self.user_request}

            【利用可能なテナント情報】
            {self.format_tenant_data()}

            ===== Swarm並行分析開始 =====
            各Swarmエージェントは独立して分析し、それぞれの専門視点から提案を作成してください。
            他のエージェントの発言に影響されず、自分の専門分野に特化した最適解を提示してください。
            最終的にマスター・シンセサイザーが全ての提案を統合します。
        """
            
        # 4. Swarm形式のグループチャット
        agents = [
            self.active_researcher,
            self.relaxation_curator,
            self.trend_innovator,
            self.efficiency_expert,
            self.culture_gourmet_explorer,
            self.master_synthesizer
        ]
        
        # Swarm設定（最大自由度で並行議論）
        groupchat = autogen.GroupChat(
            agents=agents,
            messages=[],
            max_round=12,  # 各エージェントが十分に発言できる回数
            speaker_selection_method="auto",  # 自由な発言順序
            allow_repeat_speaker=True  # 同じエージェントの複数回発言を許可
        )
        
        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config=llm_config,
            system_message="""
                あなたはSwarm方式の会議進行管理者です。
                各Swarmエージェントが独立して分析し、自由に議論できるよう調整してください。

                Swarm進行方針:
                - 各エージェントの独立性を重視
                - 多様な視点からの並行分析を促進
                - 創発的なアイデアの生成を支援
                - 最終的にマスター・シンセサイザーによる統合を実現

                自由で創造的な議論環境を提供し、多角的な提案の生成を支援してください。
            """
        )
        
        # 会議開始
        self.user_proxy.initiate_chat(
            manager,
            message=base_context,
            clear_history=True
        )
        
        print("\n" + "="*60)
        print("Swarm方式会議が終了しました。")
        print("="*60)

def main():
    """メイン関数"""
    print("竹芝ポートシティ Swarm マルチエージェントシステムを開始します...")
    
    try:
        # システム初期化
        recommendation_system = TakeshibaSwarmSystem()
        
        # Swarm議論開始
        recommendation_system.start_swarm_discussion()
        
    except KeyboardInterrupt:
        print("\n\nシステムを終了します。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    main()