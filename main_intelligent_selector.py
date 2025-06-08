"""インテリジェントGroupChat選択システム - 竹芝ポートシティレコメンドシステム"""

import os
import autogen
from dotenv import load_dotenv
from data.takeshiba_tenants import TAKESHIBA_TENANTS
from utils.weather_service import WeatherService

# 各方式のインポート
from main_round_robin import TakeshibaRoundRobinSystem
from main_selector import TakeshibaSelectorSystem  
from main_swarm import TakeshibaSwarmSystem

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
    "temperature": 0.3,  # 選択の一貫性のため低めに設定
}

# 天気サービス初期化
weather_service = WeatherService()

class IntelligentGroupChatSelector:
    def __init__(self):
        self.setup_selector_agent()
        self.systems = {
            "round_robin": TakeshibaRoundRobinSystem(),
            "selector": TakeshibaSelectorSystem(),
            "swarm": TakeshibaSwarmSystem()
        }
        self.weather_info = None
    
    def setup_selector_agent(self):
        """GroupChat方式選択エージェントをセットアップ"""
        
        self.groupchat_selector = autogen.AssistantAgent(
            name="GroupChat選択エージェント",
            llm_config=llm_config,
            system_message="""
                あなたはユーザーの要望を分析し、最適なGroupChat方式を選択する専門エージェントです。

                【3つのGroupChat方式の特徴】

                1. ROUND_ROBIN方式:
                特徴: 順番制の構造化された議論
                適用場面:
                - 初回訪問や包括的な案内が必要
                - 複数の要素を体系的に整理したい
                - 家族連れや多世代での利用
                - 「全体的に」「包括的に」「詳しく教えて」などの表現
                - 複雑で多面的な要求

                2. SELECTOR方式:
                特徴: 文脈に応じて最適な専門家を自動選択
                適用場面:
                - 特定分野への明確な要望
                - 効率性を重視する場合
                - 単一カテゴリの深掘り
                - 「ランチ」「ショッピング」「映画」など具体的な要望
                - 時間制約がある場合

                3. SWARM方式:
                特徴: 並行独立分析後の統合
                適用場面:
                - 革新的で創造的な提案が欲しい
                - 特別な日や記念日
                - 「新しい体験」「面白い」「ユニーク」などの表現
                - 複数の選択肢を比較検討したい
                - 従来にない提案を求める場合

                【分析指標】
                - 要望の具体性（具体的→SELECTOR、抽象的→SWARM）
                - 対象範囲（特定分野→SELECTOR、包括的→ROUND_ROBIN）
                - 創造性要求（高い→SWARM、標準→ROUND_ROBIN）
                - 効率重視度（高い→SELECTOR、標準→ROUND_ROBIN）
                - 特別感（重要→SWARM、通常→他方式）

                回答形式は必ず以下のJSONフォーマットで返してください:
                {
                    "selected_method": "round_robin" | "selector" | "swarm",
                    "confidence": 0.0-1.0,
                    "reasoning": "選択理由の詳細説明",
                    "user_request_analysis": "ユーザー要望の分析結果"
                }
        """)
        
        self.user_proxy = autogen.UserProxyAgent(
            name="分析コーディネーター",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config=False,
        )

    def get_weather_info(self):
        """現在の天気情報を取得"""
        return weather_service.get_current_weather()

    def get_user_request(self):
        """ユーザーからの要望を取得"""
        print("""
            === インテリジェント GroupChat選択システム ===

            AIがあなたの要望を分析し、最適なGroupChat方式を自動選択します！

            🔄 Round Robin: 構造化された包括的な提案
            🎯 Selector: 専門特化の効率的な対応  
            🌊 Swarm: 創発的で革新的なアイデア

            どのような要望でも、最適な方式で対応いたします。
        """)
        
        # デモモード用の環境変数チェック
        demo_request = os.getenv("DEMO_REQUEST")
        if demo_request:
            print(f"\n[デモモード] ユーザー要望: {demo_request}")
            return demo_request
        
        user_input = input("\nあなたのご要望をお聞かせください: ")
        return user_input

    def analyze_user_request(self, user_request):
        """ユーザー要望を分析してGroupChat方式を選択"""
        
        analysis_prompt = f"""
            以下のユーザー要望を分析し、最適なGroupChat方式を選択してください。

            【ユーザー要望】
            {user_request}

            【現在の天気情報】
            - 天気: {self.weather_info['description']}
            - 気温: {self.weather_info['temperature']}°C
            - 湿度: {self.weather_info['humidity']}%

            【分析観点】
            1. 要望の具体性レベル
            2. 対象となる分野の範囲
            3. 創造性・革新性の要求度
            4. 効率性の重要度
            5. 特別感・ユニークさの要求

            上記を総合的に分析し、最適なGroupChat方式を選択してください。
            必ずJSONフォーマットで回答してください。
        """
        
        # 分析実行
        response = self.user_proxy.initiate_chat(
            self.groupchat_selector,
            message=analysis_prompt,
            max_turns=1,
            silent=True
        )
        
        # 応答からJSONを抽出
        if hasattr(response, 'chat_history') and response.chat_history:
            last_message = response.chat_history[-1]
            if 'content' in last_message:
                return self.parse_selection_response(last_message['content'])
        
        # フォールバック: デフォルト選択
        return {
            "selected_method": "selector",
            "confidence": 0.5,
            "reasoning": "分析に失敗したため、汎用的なSelector方式を選択",
            "user_request_analysis": "分析不可"
        }

    def parse_selection_response(self, response_content):
        """選択エージェントの応答をパース"""
        import json
        import re
        
        try:
            # JSONブロックを抽出
            json_match = re.search(r'\{[^}]*\}', response_content, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
        except:
            pass
        
        # JSON抽出に失敗した場合のフォールバック分析
        response_lower = response_content.lower()
        
        if "round_robin" in response_lower or "round-robin" in response_lower:
            method = "round_robin"
        elif "swarm" in response_lower:
            method = "swarm"
        else:
            method = "selector"
        
        return {
            "selected_method": method,
            "confidence": 0.7,
            "reasoning": f"テキスト分析により{method}方式を選択",
            "user_request_analysis": "自動分析結果"
        }

    def execute_selected_method(self, selection_result, user_request):
        """選択された方式でシステムを実行"""
        
        method = selection_result["selected_method"]
        confidence = selection_result["confidence"]
        reasoning = selection_result["reasoning"]
        
        print(f"\n{'='*70}")
        print(f"🤖 AI分析結果: {method.upper()}方式を選択")
        print(f"📊 信頼度: {confidence:.1%}")
        print(f"💭 選択理由: {reasoning}")
        print(f"{'='*70}")
        
        # 選択された方式でシステム実行
        if method == "round_robin":
            print("\n🔄 Round Robin方式でシステムを実行します...")
            # ユーザー要望を環境変数に設定
            os.environ["DEMO_REQUEST"] = user_request
            self.systems["round_robin"].start_round_robin_discussion()
            
        elif method == "selector":
            print("\n🎯 Selector方式でシステムを実行します...")
            os.environ["DEMO_REQUEST"] = user_request
            self.systems["selector"].start_selector_discussion()
            
        elif method == "swarm":
            print("\n🌊 Swarm方式でシステムを実行します...")
            os.environ["DEMO_REQUEST"] = user_request
            self.systems["swarm"].start_swarm_discussion()
            
        # 環境変数をクリア
        if "DEMO_REQUEST" in os.environ:
            del os.environ["DEMO_REQUEST"]

    def start_intelligent_system(self):
        """インテリジェントシステムを開始"""
        
        try:
            # 1. 天気情報取得
            self.weather_info = self.get_weather_info()
            
            # 2. ユーザー要望取得
            user_request = self.get_user_request()
            
            print(f"\n🔍 ユーザー要望を分析中...")
            print(f"💭 要望内容: 「{user_request}」")
            
            # 3. 要望分析とGroupChat方式選択
            selection_result = self.analyze_user_request(user_request)
            
            # 4. 選択された方式でシステム実行
            self.execute_selected_method(selection_result, user_request)
            
            print(f"\n{'='*70}")
            print("🎉 インテリジェントシステムが正常に完了しました！")
            print("💡 AI分析により最適な方式での提案が完了しました。")
            print(f"{'='*70}")
            
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")
            print("フォールバックとしてSelector方式で実行します...")
            
            # フォールバック実行
            try:
                os.environ["DEMO_REQUEST"] = user_request if 'user_request' in locals() else "システムエラーのため一般的な提案をお願いします"
                self.systems["selector"].start_selector_discussion()
                if "DEMO_REQUEST" in os.environ:
                    del os.environ["DEMO_REQUEST"]
            except:
                print("フォールバック実行も失敗しました。")

def main():
    """メイン関数"""
    print("🚀 竹芝ポートシティ インテリジェントGroupChat選択システムを開始します...")
    
    try:
        # システム初期化
        intelligent_system = IntelligentGroupChatSelector()
        
        # インテリジェントシステム開始
        intelligent_system.start_intelligent_system()
        
    except KeyboardInterrupt:
        print("\n\nシステムを終了します。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    main()