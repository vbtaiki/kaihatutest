"""
バリューブックス 買取価格シミュレーター
利益率と回転率の最適解を探る

使い方:
  python simulator.py
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Tuple
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


@dataclass
class PricingConfig:
    """価格決定の係数設定"""
    # 状態ランク係数
    condition_rates: dict = None
    # 在庫日数係数（日数が増えるほど係数が下がる）
    inventory_decay_rate: float = 0.005  # 1日あたりの減少率
    # ベース買取率（定価に対する割合）
    base_purchase_rate: float = 0.30
    # カテゴリ別係数
    category_rates: dict = None
    
    def __post_init__(self):
        if self.condition_rates is None:
            self.condition_rates = {
                'S': 1.2,   # 新品同様
                'A': 1.0,   # 良好
                'B': 0.75,  # 並
                'C': 0.4    # 難あり
            }
        if self.category_rates is None:
            self.category_rates = {
                '文学': 0.9,
                'ビジネス': 1.1,
                '教養': 1.0,
                '技術書': 1.3
            }


def calculate_purchase_price(
    list_price: int,
    condition: str,
    inventory_days: int,
    category: str,
    config: PricingConfig
) -> int:
    """
    買取価格を計算する
    
    計算式:
    買取価格 = 定価 × ベース買取率 × 状態係数 × 在庫日数係数 × カテゴリ係数
    """
    base_price = list_price * config.base_purchase_rate
    condition_factor = config.condition_rates.get(condition, 0.5)
    
    # 在庫日数係数: 30日を境に係数が下がり始める
    if inventory_days <= 30:
        inventory_factor = 1.0
    else:
        inventory_factor = max(0.5, 1.0 - (inventory_days - 30) * config.inventory_decay_rate)
    
    category_factor = config.category_rates.get(category, 1.0)
    
    purchase_price = base_price * condition_factor * inventory_factor * category_factor
    
    return int(purchase_price)


def estimate_selling_price(purchase_price: int, category: str) -> int:
    """販売予想価格を算出（買取価格の2.0〜2.5倍）"""
    multipliers = {
        '文学': 2.2,
        'ビジネス': 2.0,
        '教養': 2.1,
        '技術書': 2.3
    }
    multiplier = multipliers.get(category, 2.1)
    return int(purchase_price * multiplier)


def simulate_profit(config: PricingConfig, data: pd.DataFrame) -> dict:
    """
    指定の係数設定でシミュレーションを実行
    """
    results = []
    
    for _, row in data.iterrows():
        new_purchase = calculate_purchase_price(
            list_price=row['定価'],
            condition=row['状態ランク'],
            inventory_days=row['在庫日数'],
            category=row['カテゴリ'],
            config=config
        )
        new_selling = estimate_selling_price(new_purchase, row['カテゴリ'])
        
        results.append({
            '書籍名': row['書籍名'],
            '現在_買取': row['買取価格'],
            '新_買取': new_purchase,
            '買取差額': new_purchase - row['買取価格'],
            '現在_販売': row['販売価格'],
            '新_販売': new_selling,
            '現在_粗利': row['粗利'],
            '新_粗利': new_selling - new_purchase if row['販売済'] else 0,
            '販売済': row['販売済']
        })
    
    df_results = pd.DataFrame(results)
    
    # 販売済みデータのみで集計
    sold = df_results[df_results['販売済'] == 1]
    
    return {
        'total_current_profit': sold['現在_粗利'].sum(),
        'total_new_profit': sold['新_粗利'].sum(),
        'profit_change': sold['新_粗利'].sum() - sold['現在_粗利'].sum(),
        'avg_purchase_change': df_results['買取差額'].mean(),
        'details': df_results
    }


def run_sensitivity_analysis(data: pd.DataFrame) -> pd.DataFrame:
    """
    ベース買取率を変化させて利益への影響を分析
    """
    results = []
    
    for rate in np.arange(0.20, 0.45, 0.02):
        config = PricingConfig(base_purchase_rate=rate)
        sim = simulate_profit(config, data)
        
        results.append({
            'ベース買取率': f"{rate:.0%}",
            '総粗利': sim['total_new_profit'],
            '粗利変化': sim['profit_change'],
            '平均買取変化': sim['avg_purchase_change']
        })
    
    return pd.DataFrame(results)


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║     📊 バリューブックス 買取価格シミュレーター               ║
║     利益率と回転率の最適解を探る                             ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # データ読み込み
    data_path = os.path.join(DATA_DIR, 'historical_data.csv')
    data = pd.read_csv(data_path)
    print(f"📁 データ読み込み完了: {len(data)}件")
    print(f"{'='*60}\n")
    
    # 現在の設定でシミュレーション
    print("【現在の係数設定でシミュレーション】")
    current_config = PricingConfig()
    print(f"  ベース買取率: {current_config.base_purchase_rate:.0%}")
    print(f"  状態係数: {current_config.condition_rates}")
    print(f"  在庫減衰率: {current_config.inventory_decay_rate}/日")
    
    result = simulate_profit(current_config, data)
    print(f"\n  現在の総粗利: ¥{result['total_current_profit']:,}")
    print(f"  新設定での総粗利: ¥{result['total_new_profit']:,}")
    print(f"  変化額: ¥{result['profit_change']:+,}")
    
    # 感度分析
    print(f"\n{'='*60}")
    print("【ベース買取率の感度分析】")
    print("  ※ 買取率を変化させた場合の粗利への影響\n")
    
    sensitivity = run_sensitivity_analysis(data)
    print(sensitivity.to_string(index=False))
    
    # 詳細結果
    print(f"\n{'='*60}")
    print("【書籍別 シミュレーション詳細】\n")
    
    details = result['details'][['書籍名', '現在_買取', '新_買取', '買取差額', '現在_粗利', '新_粗利']].head(10)
    print(details.to_string(index=False))
    
    # 最適化提案
    print(f"\n{'='*60}")
    print("【最適化の提案】")
    
    best_row = sensitivity.loc[sensitivity['総粗利'].idxmax()]
    print(f"\n  💡 推奨ベース買取率: {best_row['ベース買取率']}")
    print(f"     → 総粗利が最大化される設定")
    
    print(f"\n  📈 カテゴリ別の考察:")
    for cat in data['カテゴリ'].unique():
        cat_data = data[data['カテゴリ'] == cat]
        avg_profit = cat_data['粗利'].mean()
        avg_days = cat_data['在庫日数'].mean()
        print(f"     {cat}: 平均粗利¥{avg_profit:,.0f} / 平均在庫{avg_days:.0f}日")


if __name__ == "__main__":
    main()



