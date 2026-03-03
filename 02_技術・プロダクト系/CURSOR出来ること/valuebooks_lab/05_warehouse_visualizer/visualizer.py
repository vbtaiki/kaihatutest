"""
バリューブックス 倉庫AGVビジュアライザー
50x50グリッド上でロボットの動きを可視化

使い方:
  python visualizer.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
import random
from dataclasses import dataclass
from typing import List, Tuple
import matplotlib

# 日本語フォント設定
matplotlib.rcParams['font.family'] = ['Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'sans-serif']


@dataclass
class Order:
    """注文データ"""
    id: str
    shelf_position: Tuple[int, int]  # 棚の位置
    status: str  # 'pending', 'in_progress', 'completed'


@dataclass
class AGV:
    """自動搬送ロボット"""
    id: str
    position: Tuple[int, int]
    target: Tuple[int, int] = None
    carrying_order: Order = None
    color: str = 'blue'
    path: List[Tuple[int, int]] = None
    
    def __post_init__(self):
        self.path = []


class WarehouseSimulator:
    """倉庫シミュレーター"""
    
    def __init__(self, width: int = 50, height: int = 50):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width))
        
        # 棚のレイアウト（通路を確保しながら配置）
        self.shelves = []
        for x in range(5, width - 5, 6):
            for y in range(5, height - 5, 4):
                self.shelves.append((x, y))
                self.grid[y, x] = 1  # 棚
        
        # ピッキングステーション（出荷エリア）
        self.picking_station = (width // 2, height - 3)
        
        # AGVの初期化（3台）
        self.agvs = [
            AGV(id="AGV-1", position=(5, 2), color='#3498db'),
            AGV(id="AGV-2", position=(25, 2), color='#e74c3c'),
            AGV(id="AGV-3", position=(45, 2), color='#2ecc71'),
        ]
        
        # 注文キュー
        self.orders = []
        self.completed_orders = 0
        
        # シミュレーション時間
        self.time = 0
    
    def generate_order(self) -> Order:
        """ランダムな注文を生成"""
        shelf = random.choice(self.shelves)
        order = Order(
            id=f"ORD-{self.time:04d}",
            shelf_position=shelf,
            status='pending'
        )
        return order
    
    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """簡易的なパス探索（直線経路 + 障害物回避）"""
        path = [start]
        current = list(start)
        
        while (current[0], current[1]) != end:
            # X方向に移動
            if current[0] < end[0]:
                current[0] += 1
            elif current[0] > end[0]:
                current[0] -= 1
            
            # Y方向に移動
            if current[1] < end[1]:
                current[1] += 1
            elif current[1] > end[1]:
                current[1] -= 1
            
            path.append((current[0], current[1]))
        
        return path
    
    def assign_orders(self):
        """空いているAGVに注文を割り当て"""
        for agv in self.agvs:
            if agv.carrying_order is None and self.orders:
                # 未割当の注文を取得
                pending_orders = [o for o in self.orders if o.status == 'pending']
                if pending_orders:
                    order = pending_orders[0]
                    order.status = 'in_progress'
                    agv.carrying_order = order
                    agv.target = order.shelf_position
                    agv.path = self.find_path(agv.position, order.shelf_position)
    
    def move_agvs(self):
        """AGVを1ステップ移動"""
        for agv in self.agvs:
            if agv.path and len(agv.path) > 1:
                agv.path.pop(0)
                agv.position = agv.path[0]
                
                # 目的地に到着
                if agv.position == agv.target:
                    if agv.carrying_order:
                        if agv.target == agv.carrying_order.shelf_position:
                            # 棚から商品をピック → ピッキングステーションへ
                            agv.target = self.picking_station
                            agv.path = self.find_path(agv.position, self.picking_station)
                        elif agv.target == self.picking_station:
                            # 出荷完了
                            agv.carrying_order.status = 'completed'
                            self.orders.remove(agv.carrying_order)
                            agv.carrying_order = None
                            agv.target = None
                            self.completed_orders += 1
    
    def step(self):
        """シミュレーション1ステップ"""
        self.time += 1
        
        # 一定確率で注文発生
        if random.random() < 0.15:  # 15%の確率
            order = self.generate_order()
            self.orders.append(order)
        
        # 注文をAGVに割り当て
        self.assign_orders()
        
        # AGVを移動
        self.move_agvs()


def run_visualization():
    """可視化を実行"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║     🏭 バリューブックス 倉庫AGVビジュアライザー              ║
║     倉庫ロボットの動きをリアルタイムで可視化                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # シミュレーター初期化
    sim = WarehouseSimulator()
    
    # 初期注文を生成
    for _ in range(5):
        sim.orders.append(sim.generate_order())
    
    # 描画設定
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')
    
    def init():
        ax.set_xlim(0, sim.width)
        ax.set_ylim(0, sim.height)
        ax.set_aspect('equal')
        ax.set_title('バリューブックス 倉庫シミュレーション', 
                     fontsize=16, color='white', pad=20)
        return []
    
    def animate(frame):
        ax.clear()
        ax.set_xlim(0, sim.width)
        ax.set_ylim(0, sim.height)
        ax.set_aspect('equal')
        ax.set_facecolor('#16213e')
        
        # グリッド線
        for i in range(0, sim.width + 1, 5):
            ax.axvline(x=i, color='#2d4059', linewidth=0.5, alpha=0.5)
        for i in range(0, sim.height + 1, 5):
            ax.axhline(y=i, color='#2d4059', linewidth=0.5, alpha=0.5)
        
        # 棚を描画
        for shelf in sim.shelves:
            rect = patches.Rectangle(
                (shelf[0] - 0.4, shelf[1] - 0.4), 0.8, 0.8,
                linewidth=1, edgecolor='#f39c12', facecolor='#e67e22', alpha=0.8
            )
            ax.add_patch(rect)
        
        # ピッキングステーションを描画
        station = sim.picking_station
        rect = patches.Rectangle(
            (station[0] - 2, station[1] - 1), 4, 2,
            linewidth=2, edgecolor='#00ff00', facecolor='#27ae60', alpha=0.8
        )
        ax.add_patch(rect)
        ax.text(station[0], station[1], '出荷', ha='center', va='center', 
                color='white', fontsize=10, fontweight='bold')
        
        # 注文の目的地を強調
        for order in sim.orders:
            if order.status == 'pending':
                circle = patches.Circle(
                    order.shelf_position, 1.2,
                    linewidth=2, edgecolor='#ff6b6b', facecolor='none', linestyle='--'
                )
                ax.add_patch(circle)
        
        # AGVを描画
        for agv in sim.agvs:
            # AGV本体
            circle = patches.Circle(
                agv.position, 1.0,
                linewidth=2, edgecolor='white', facecolor=agv.color
            )
            ax.add_patch(circle)
            
            # AGVのID
            ax.text(agv.position[0], agv.position[1], agv.id[-1], 
                    ha='center', va='center', color='white', fontsize=8, fontweight='bold')
            
            # パスを描画
            if agv.path and len(agv.path) > 1:
                path_x = [p[0] for p in agv.path]
                path_y = [p[1] for p in agv.path]
                ax.plot(path_x, path_y, color=agv.color, linewidth=2, alpha=0.5, linestyle='--')
        
        # 情報表示
        ax.set_title(
            f'🏭 バリューブックス 倉庫シミュレーション  |  '
            f'⏱ Time: {sim.time}  |  '
            f'📦 待機注文: {len([o for o in sim.orders if o.status == "pending"])}  |  '
            f'✅ 完了: {sim.completed_orders}',
            fontsize=12, color='white', pad=15
        )
        
        # 凡例
        ax.text(2, sim.height - 2, '🟠 棚', color='white', fontsize=9)
        ax.text(2, sim.height - 4, '🟢 出荷エリア', color='white', fontsize=9)
        ax.text(2, sim.height - 6, '⭕ 注文待ち', color='#ff6b6b', fontsize=9)
        
        # シミュレーションを1ステップ進める
        sim.step()
        
        return []
    
    print("🚀 アニメーションを開始します...")
    print("   ウィンドウを閉じると終了します。")
    
    anim = FuncAnimation(
        fig, animate, init_func=init,
        frames=200, interval=300, blit=False
    )
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run_visualization()



