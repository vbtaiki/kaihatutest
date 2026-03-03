"""
バリューブックス メール配信ダッシュボード
ブラウザで結果を確認できるUI

使い方:
  streamlit run 08_email_optimizer/dashboard.py
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="メール配信最適化",
    page_icon="📧",
    layout="wide"
)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a5f;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
    }
    .email-preview {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .rank-platinum { color: #9333ea; font-weight: bold; }
    .rank-gold { color: #f59e0b; font-weight: bold; }
    .rank-silver { color: #6b7280; font-weight: bold; }
    .rank-bronze { color: #b45309; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def load_data():
    """データを読み込む"""
    targets_path = os.path.join(DATA_DIR, 'today_targets.csv')
    emails_path = os.path.join(DATA_DIR, 'generated_emails.json')
    
    targets = None
    emails = None
    
    if os.path.exists(targets_path):
        targets = pd.read_csv(targets_path)
    
    if os.path.exists(emails_path):
        with open(emails_path, 'r', encoding='utf-8') as f:
            emails = json.load(f)
    
    return targets, emails

def get_rank_style(rank):
    """ランクに応じたスタイルクラスを返す"""
    styles = {
        'プラチナ': 'rank-platinum',
        'ゴールド': 'rank-gold',
        'シルバー': 'rank-silver',
        'ブロンズ': 'rank-bronze'
    }
    return styles.get(rank, '')

def main():
    st.markdown('<p class="main-header">📧 メール配信最適化ダッシュボード</p>', unsafe_allow_html=True)
    st.markdown("最小限のメールで最大の効果を実現")
    
    targets, emails = load_data()
    
    if targets is None:
        st.warning("まだデータがありません。先に `python3 08_email_optimizer/optimizer.py` を実行してください。")
        return
    
    # サマリーメトリクス
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📨 送信予定数", f"{len(targets)}通")
    
    with col2:
        expected = targets['期待転換率'].sum() * len(targets) if '期待転換率' in targets.columns else 0
        st.metric("🎯 期待申込数", f"{expected:.1f}件")
    
    with col3:
        avg_score = targets['スコア'].mean() if 'スコア' in targets.columns else 0
        st.metric("📊 平均スコア", f"{avg_score:.1f}")
    
    with col4:
        platinum_count = len(targets[targets['会員ランク'] == 'プラチナ']) if '会員ランク' in targets.columns else 0
        st.metric("👑 VIP顧客", f"{platinum_count}名")
    
    # タブで表示を切り替え
    tab1, tab2, tab3 = st.tabs(["📋 抽出顧客一覧", "✉️ 生成メール確認", "📊 分析"])
    
    with tab1:
        st.markdown("### 抽出された顧客リスト")
        st.markdown("スコアが高い順に並んでいます")
        
        # ランクでフィルタ
        ranks = ['すべて'] + targets['会員ランク'].unique().tolist()
        selected_rank = st.selectbox("ランクでフィルタ", ranks)
        
        display_df = targets if selected_rank == 'すべて' else targets[targets['会員ランク'] == selected_rank]
        
        # 表示するカラムを選択
        display_cols = ['顧客ID', '氏名', '会員ランク', '得意ジャンル', '休眠日数', 'スコア']
        available_cols = [c for c in display_cols if c in display_df.columns]
        
        st.dataframe(
            display_df[available_cols],
            use_container_width=True,
            hide_index=True
        )
    
    with tab2:
        st.markdown("### 生成されたメール")
        
        if emails is None:
            st.info("メールがまだ生成されていません。`python3 08_email_optimizer/email_generator.py` を実行してください。")
        else:
            # 顧客を選択
            email_options = [f"{e['customer_id']} - {e['to'].split('@')[0]}... ({e['rank']})" for e in emails]
            selected_email_idx = st.selectbox("顧客を選択", range(len(emails)), format_func=lambda x: email_options[x])
            
            email = emails[selected_email_idx]
            
            st.markdown("---")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**📬 宛先**")
                st.code(email['to'])
                
                st.markdown("**🏷️ 会員ランク**")
                st.markdown(f"<span class='{get_rank_style(email['rank'])}'>{email['rank']}</span>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("**📝 件名**")
                st.info(email['subject'])
                
                st.markdown("**📄 本文**")
                st.text_area("", email['body'], height=300, disabled=True)
            
            # 送信ボタン（デモ）
            if st.button("📤 このメールを送信（デモ）", type="primary"):
                st.success(f"✅ {email['to']} へメールを送信しました（デモ）")
    
    with tab3:
        st.markdown("### ランク別分析")
        
        if '会員ランク' in targets.columns:
            rank_counts = targets['会員ランク'].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ランク別人数")
                st.bar_chart(rank_counts)
            
            with col2:
                st.markdown("#### ランク別の詳細")
                for rank in rank_counts.index:
                    rank_data = targets[targets['会員ランク'] == rank]
                    avg_dormant = rank_data['休眠日数'].mean() if '休眠日数' in rank_data.columns else 0
                    
                    st.markdown(f"""
                    **{rank}** ({rank_counts[rank]}名)
                    - 平均休眠日数: {avg_dormant:.0f}日
                    """)
        
        st.markdown("---")
        st.markdown("### 休眠日数の分布")
        
        if '休眠日数' in targets.columns:
            st.bar_chart(targets['休眠日数'].value_counts().sort_index())
    
    # フッター
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #718096; font-size: 0.9rem;">
        📚 バリューブックス メール配信最適化システム | Powered by Cursor
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()



