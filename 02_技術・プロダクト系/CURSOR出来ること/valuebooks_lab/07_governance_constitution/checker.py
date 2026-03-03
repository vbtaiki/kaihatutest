"""
バリューブックス 憲法チェッカー
案件条件を入力すると、憲法に照らして必要なプロセスを出力

使い方:
  python checker.py
"""

import json
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class DecisionLevel(Enum):
    """意思決定レベル"""
    A = "日常"      # 担当者の裁量
    B = "通常"      # 上長承認
    C = "重要"      # 経営会議承認
    D = "最重要"    # 全体投票


@dataclass
class ApprovalProcess:
    """承認プロセス"""
    level: DecisionLevel
    required_approval: str
    steps: List[str]
    timeline: str
    voting_threshold: Optional[str] = None


# 憲法に基づくルール定義
CONSTITUTION_RULES = {
    "decision_levels": {
        DecisionLevel.A: {
            "examples": ["仕入れ判断", "顧客対応", "日常業務"],
            "approval": "担当者の裁量",
            "amount_threshold": 0
        },
        DecisionLevel.B: {
            "examples": ["10万円未満の支出", "人員配置", "備品購入"],
            "approval": "上長承認",
            "amount_threshold": 100000
        },
        DecisionLevel.C: {
            "examples": ["100万円以上の投資", "新規事業", "大型契約"],
            "approval": "経営会議承認",
            "amount_threshold": 1000000
        },
        DecisionLevel.D: {
            "examples": ["M&A", "大規模組織変更", "事業売却", "合併"],
            "approval": "全体投票（貢献係数に比例）",
            "amount_threshold": float('inf'),
            "voting_threshold": "2/3以上の賛成"
        }
    },
    "ma_criteria": {
        "cultural_fit": ["本", "出版", "文化", "持続可能性"],
        "financial_health": {
            "max_debt_ratio": 200,
            "min_growth_rate": 0
        },
        "synergy": ["補完", "コスト削減", "売上増加"]
    }
}


def determine_decision_level(
    amount: float,
    is_ma: bool = False,
    is_org_change: bool = False
) -> DecisionLevel:
    """案件の決定レベルを判定"""
    
    # M&Aや大規模組織変更は自動的にレベルD
    if is_ma or is_org_change:
        return DecisionLevel.D
    
    # 金額による判定
    if amount >= 1000000:
        return DecisionLevel.C
    elif amount >= 100000:
        return DecisionLevel.B
    else:
        return DecisionLevel.A


def get_approval_process(level: DecisionLevel) -> ApprovalProcess:
    """決定レベルに応じた承認プロセスを取得"""
    
    processes = {
        DecisionLevel.A: ApprovalProcess(
            level=DecisionLevel.A,
            required_approval="担当者の裁量で決定可能",
            steps=[
                "✅ 担当者が判断・実行",
                "✅ 必要に応じて上長に報告"
            ],
            timeline="即時"
        ),
        DecisionLevel.B: ApprovalProcess(
            level=DecisionLevel.B,
            required_approval="直属の上長による承認",
            steps=[
                "1️⃣ 担当者が申請書を作成",
                "2️⃣ 上長に承認依頼",
                "3️⃣ 上長が承認・却下を判断",
                "4️⃣ 承認後、実行"
            ],
            timeline="1〜3営業日"
        ),
        DecisionLevel.C: ApprovalProcess(
            level=DecisionLevel.C,
            required_approval="経営会議での承認",
            steps=[
                "1️⃣ 提案書の作成（目的・費用・効果を明記）",
                "2️⃣ 上長の事前確認",
                "3️⃣ 経営会議への上程（週次開催）",
                "4️⃣ 経営会議での審議・決議",
                "5️⃣ 承認後、実行計画策定"
            ],
            timeline="1〜2週間"
        ),
        DecisionLevel.D: ApprovalProcess(
            level=DecisionLevel.D,
            required_approval="全構成員による投票（貢献係数に比例した投票権）",
            steps=[
                "【提案段階】",
                "1️⃣ 案件概要書の作成",
                "2️⃣ 財務・法務デューデリジェンスの実施",
                "",
                "【審議段階】",
                "3️⃣ 全構成員への情報開示（議決14日以上前）",
                "4️⃣ 質疑応答期間（7日間）",
                "5️⃣ 経営会議による事前審査",
                "",
                "【議決段階】",
                "6️⃣ 全体投票の実施（5営業日間）",
                "7️⃣ 貢献係数に基づく投票権で集計",
                "8️⃣ 2/3以上の賛成で可決",
                "",
                "【実行段階】",
                "9️⃣ 可決後30日以内に実行計画策定",
                "🔟 四半期ごとの進捗報告"
            ],
            timeline="最短1ヶ月",
            voting_threshold="総投票権の2/3以上の賛成が必要"
        )
    }
    
    return processes[level]


def check_ma_criteria(
    business_type: str,
    debt_ratio: float,
    growth_rate: float,
    synergy_description: str
) -> dict:
    """M&A対象企業の選定基準をチェック"""
    
    results = {
        "cultural_fit": {
            "passed": False,
            "reason": ""
        },
        "financial_health": {
            "passed": False,
            "reason": ""
        },
        "synergy": {
            "passed": False,
            "reason": ""
        }
    }
    
    # 文化的適合性チェック
    keywords = CONSTITUTION_RULES["ma_criteria"]["cultural_fit"]
    if any(kw in business_type for kw in keywords):
        results["cultural_fit"]["passed"] = True
        results["cultural_fit"]["reason"] = "事業内容が企業理念と適合"
    else:
        results["cultural_fit"]["reason"] = f"事業内容が企業理念と適合しない可能性（キーワード: {', '.join(keywords)}）"
    
    # 財務健全性チェック
    criteria = CONSTITUTION_RULES["ma_criteria"]["financial_health"]
    if debt_ratio <= criteria["max_debt_ratio"] and growth_rate >= criteria["min_growth_rate"]:
        results["financial_health"]["passed"] = True
        results["financial_health"]["reason"] = f"負債比率{debt_ratio}%、成長率{growth_rate}%で基準を満たす"
    else:
        issues = []
        if debt_ratio > criteria["max_debt_ratio"]:
            issues.append(f"負債比率{debt_ratio}%（上限{criteria['max_debt_ratio']}%）")
        if growth_rate < criteria["min_growth_rate"]:
            issues.append(f"成長率{growth_rate}%（最低{criteria['min_growth_rate']}%）")
        results["financial_health"]["reason"] = "基準未達: " + ", ".join(issues)
    
    # シナジー効果チェック
    synergy_keywords = CONSTITUTION_RULES["ma_criteria"]["synergy"]
    if any(kw in synergy_description for kw in synergy_keywords):
        results["synergy"]["passed"] = True
        results["synergy"]["reason"] = "具体的なシナジー効果が見込める"
    else:
        results["synergy"]["reason"] = "シナジー効果の具体性が不足"
    
    return results


def print_divider():
    print("=" * 60)


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║     📜 バリューブックス 憲法チェッカー                       ║
║     案件条件から必要な承認プロセスを判定                     ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        print_divider()
        print("\n【案件タイプを選択】")
        print("1. 一般案件（金額ベースで判定）")
        print("2. M&A案件（特別審査）")
        print("3. 組織変更案件")
        print("0. 終了")
        
        choice = input("\n選択 (0-3): ").strip()
        
        if choice == "0":
            print("\n👋 チェッカーを終了します")
            break
        
        elif choice == "1":
            print("\n【一般案件の情報を入力】")
            try:
                amount = float(input("金額（円）: "))
            except ValueError:
                print("⚠️ 無効な金額です")
                continue
            
            level = determine_decision_level(amount)
            process = get_approval_process(level)
            
            print(f"\n{'='*60}")
            print(f"📋 判定結果")
            print(f"{'='*60}")
            print(f"決定レベル: {level.name}（{level.value}）")
            print(f"必要な承認: {process.required_approval}")
            print(f"目安期間: {process.timeline}")
            print(f"\n【承認プロセス】")
            for step in process.steps:
                print(f"  {step}")
        
        elif choice == "2":
            print("\n【M&A案件の情報を入力】")
            business_type = input("対象企業の事業内容: ")
            
            try:
                debt_ratio = float(input("負債比率（%）: "))
                growth_rate = float(input("直近3年の売上成長率（%）: "))
            except ValueError:
                print("⚠️ 無効な数値です")
                continue
            
            synergy = input("期待されるシナジー効果: ")
            
            # M&A基準チェック
            criteria_result = check_ma_criteria(business_type, debt_ratio, growth_rate, synergy)
            
            print(f"\n{'='*60}")
            print(f"📋 M&A選定基準チェック結果")
            print(f"{'='*60}")
            
            all_passed = True
            for criterion, result in criteria_result.items():
                status = "✅ 適合" if result["passed"] else "⚠️ 要検討"
                print(f"\n【{criterion}】 {status}")
                print(f"  {result['reason']}")
                if not result["passed"]:
                    all_passed = False
            
            print(f"\n{'='*60}")
            if all_passed:
                print("✅ すべての基準を満たしています")
            else:
                print("⚠️ 一部の基準を満たしていません。経営会議での慎重な審議が必要です。")
            
            # 承認プロセスを表示
            process = get_approval_process(DecisionLevel.D)
            print(f"\n{'='*60}")
            print(f"📋 必要な承認プロセス（レベルD: {process.required_approval}）")
            print(f"{'='*60}")
            for step in process.steps:
                print(f"  {step}")
            print(f"\n⏱ 目安期間: {process.timeline}")
            print(f"🗳 議決要件: {process.voting_threshold}")
        
        elif choice == "3":
            print("\n【組織変更案件】")
            print("大規模な組織変更は自動的にレベルD（最重要）に分類されます。")
            
            process = get_approval_process(DecisionLevel.D)
            print(f"\n{'='*60}")
            print(f"📋 必要な承認プロセス")
            print(f"{'='*60}")
            for step in process.steps:
                print(f"  {step}")
            print(f"\n⏱ 目安期間: {process.timeline}")
            print(f"🗳 議決要件: {process.voting_threshold}")
        
        else:
            print("⚠️ 無効な選択です")


if __name__ == "__main__":
    main()



