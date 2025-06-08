"""3つのGroupChat方式比較システム - 竹芝ポートシティレコメンドシステム"""

import os
import sys
from dotenv import load_dotenv

# 各方式のインポート
from main_round_robin import TakeshibaRoundRobinSystem
from main_selector import TakeshibaSelectorSystem  
from main_swarm import TakeshibaSwarmSystem

# 環境変数を読み込み
load_dotenv()

class GroupChatComparison:
    def __init__(self):
        self.systems = {
            "round_robin": TakeshibaRoundRobinSystem(),
            "selector": TakeshibaSelectorSystem(),
            "swarm": TakeshibaSwarmSystem()
        }
    
    def show_comparison_menu(self):
        """比較メニューを表示"""
        print("""
=== AutoGen GroupChat方式比較システム ===
竹芝ポートシティレコメンドシステムで3つの方式を体験

【1. Round Robin方式】
特徴: 順番に発言、構造化された議論
適用: 段階的な情報構築、確実な全員参加
流れ: 天気分析 → 施設情報 → ショッピング → エンタメ → 総合統合

【2. Selector方式】  
特徴: AIが文脈に応じて最適エージェント選択
適用: 効率的な専門特化、動的な議論展開
流れ: 要望に応じて関連専門家が自動選択

【3. Swarm方式】
特徴: 並行独立分析後に統合
適用: 多角的分析、創発的アイデア生成
流れ: 5つの視点で並行分析 → 最終統合

どの方式を試してみますか？
""")
    
    def run_comparison(self):
        """比較システムを実行"""
        while True:
            try:
                self.show_comparison_menu()
                
                choice = input("""
選択してください:
1. Round Robin方式を試す
2. Selector方式を試す  
3. Swarm方式を試す
4. 全方式を連続実行（同じ要望で比較）
5. 終了

番号を入力: """)
                
                if choice == "1":
                    print("\n" + "="*70)
                    print("Round Robin方式を開始します...")
                    print("="*70)
                    self.systems["round_robin"].start_round_robin_discussion()
                    
                elif choice == "2":
                    print("\n" + "="*70)
                    print("Selector方式を開始します...")
                    print("="*70)
                    self.systems["selector"].start_selector_discussion()
                    
                elif choice == "3":
                    print("\n" + "="*70)
                    print("Swarm方式を開始します...")
                    print("="*70)
                    self.systems["swarm"].start_swarm_discussion()
                    
                elif choice == "4":
                    self.run_all_methods_comparison()
                    
                elif choice == "5":
                    print("\nシステムを終了します。お疲れ様でした！")
                    break
                    
                else:
                    print("\n無効な選択です。1-5の番号を入力してください。")
                    
            except KeyboardInterrupt:
                print("\n\nシステムを終了します。")
                break
            except Exception as e:
                print(f"\nエラーが発生しました: {e}")
                print("もう一度お試しください。")
    
    def run_all_methods_comparison(self):
        """全方式で同じ要望を処理して比較"""
        print("""
=== 全方式連続比較モード ===
同じユーザー要望を3つの方式で処理し、結果を比較します。
""")
        
        # 共通の要望を取得
        user_request = input("比較用のユーザー要望を入力してください: ")
        
        # 環境変数に設定（各システムがこれを使用）
        os.environ["DEMO_REQUEST"] = user_request
        
        print(f"\n要望「{user_request}」で3つの方式を連続実行します...\n")
        
        # 1. Round Robin方式
        print("="*80)
        print("【1/3】Round Robin方式での実行")
        print("="*80)
        try:
            self.systems["round_robin"].start_round_robin_discussion()
        except Exception as e:
            print(f"Round Robin方式でエラー: {e}")
        
        input("\n次の方式に進むにはEnterキーを押してください...")
        
        # 2. Selector方式
        print("\n" + "="*80)
        print("【2/3】Selector方式での実行")
        print("="*80)
        try:
            self.systems["selector"].start_selector_discussion()
        except Exception as e:
            print(f"Selector方式でエラー: {e}")
        
        input("\n次の方式に進むにはEnterキーを押してください...")
        
        # 3. Swarm方式
        print("\n" + "="*80)
        print("【3/3】Swarm方式での実行")
        print("="*80)
        try:
            self.systems["swarm"].start_swarm_discussion()
        except Exception as e:
            print(f"Swarm方式でエラー: {e}")
        
        print("\n" + "="*80)
        print("全方式の実行が完了しました！")
        print("="*80)
        print("""
比較ポイント:
- Round Robin: 構造化された段階的な提案構築
- Selector: 要望に特化した効率的な専門家選択  
- Swarm: 多角的な並行分析と創発的な統合

どの方式が最も良い提案を生成したかご確認ください。
""")
        
        # 環境変数をクリア
        if "DEMO_REQUEST" in os.environ:
            del os.environ["DEMO_REQUEST"]

def main():
    """メイン関数"""
    print("竹芝ポートシティ GroupChat方式比較システムを開始します...")
    
    try:
        comparison_system = GroupChatComparison()
        comparison_system.run_comparison()
        
    except KeyboardInterrupt:
        print("\n\nシステムを終了します。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    main()