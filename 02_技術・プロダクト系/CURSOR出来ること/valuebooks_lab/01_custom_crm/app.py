"""
バリューブックス カスタムCRM
Salesforce代替 - シンプルで高速な顧客管理システム
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ページ設定
st.set_page_config(
    page_title="バリューブックス CRM",
    page_icon="📚",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a365d;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #718096;
        margin-bottom: 2rem;
    }
    .customer-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1rem;
    }
    .rank-platinum { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .rank-gold { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    .rank-silver { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
    .rank-bronze { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
    .metric-box {
        background: #f7fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        border-left: 4px solid #667eea;
    }
    .interaction-item {
        padding: 0.75rem;
        border-left: 3px solid #667eea;
        margin-bottom: 0.5rem;
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# データディレクトリ
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# データ読み込み
@st.cache_data
def load_data():
    customers = pd.read_csv(os.path.join(DATA_DIR, 'customers.csv'))
    interactions = pd.read_csv(os.path.join(DATA_DIR, 'interactions.csv'))
    return customers, interactions

# メモファイルのパス
MEMO_FILE = os.path.join(DATA_DIR, 'customer_memos.csv')

def load_memos():
    if os.path.exists(MEMO_FILE):
        return pd.read_csv(MEMO_FILE)
    return pd.DataFrame(columns=['顧客ID', 'メモ日時', '担当者', 'メモ内容'])

def save_memo(customer_id, author, content):
    memos = load_memos()
    new_memo = pd.DataFrame([{
        '顧客ID': customer_id,
        'メモ日時': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '担当者': author,
        'メモ内容': content
    }])
    memos = pd.concat([memos, new_memo], ignore_index=True)
    memos.to_csv(MEMO_FILE, index=False)

def get_rank_color(rank):
    colors = {
        'プラチナ': '#667eea',
        'ゴールド': '#f5576c',
        'シルバー': '#4facfe',
        'ブロンズ': '#43e97b'
    }
    return colors.get(rank, '#718096')

def main():
    customers, interactions = load_data()
    
    # ヘッダー
    st.markdown('<p class="main-header">📚 バリューブックス CRM</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">脱SaaS - シンプルで高速な顧客管理</p>', unsafe_allow_html=True)
    
    # サイドバー：検索
    st.sidebar.header("🔍 顧客検索")
    
    search_method = st.sidebar.radio("検索方法", ["顧客IDで検索", "氏名で検索", "ランクで絞り込み"])
    
    selected_customer = None
    
    if search_method == "顧客IDで検索":
        customer_ids = customers['顧客ID'].tolist()
        selected_id = st.sidebar.selectbox("顧客ID", customer_ids)
        selected_customer = customers[customers['顧客ID'] == selected_id].iloc[0]
        
    elif search_method == "氏名で検索":
        search_name = st.sidebar.text_input("氏名を入力")
        if search_name:
            matches = customers[customers['氏名'].str.contains(search_name, na=False)]
            if len(matches) > 0:
                selected_name = st.sidebar.selectbox("該当顧客", matches['氏名'].tolist())
                selected_customer = customers[customers['氏名'] == selected_name].iloc[0]
            else:
                st.sidebar.warning("該当する顧客が見つかりません")
                
    else:  # ランクで絞り込み
        ranks = customers['会員ランク'].unique().tolist()
        selected_rank = st.sidebar.selectbox("会員ランク", ranks)
        filtered = customers[customers['会員ランク'] == selected_rank]
        if len(filtered) > 0:
            selected_name = st.sidebar.selectbox("顧客を選択", filtered['氏名'].tolist())
            selected_customer = customers[customers['氏名'] == selected_name].iloc[0]
    
    # ダッシュボード統計
    st.sidebar.markdown("---")
    st.sidebar.header("📊 ダッシュボード")
    st.sidebar.metric("総顧客数", f"{len(customers)}名")
    st.sidebar.metric("今月の対応件数", f"{len(interactions)}件")
    st.sidebar.metric("平均LTV", f"¥{customers['LTV'].mean():,.0f}")
    
    # メインコンテンツ
    if selected_customer is not None:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # 顧客カード
            rank_color = get_rank_color(selected_customer['会員ランク'])
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {rank_color} 0%, {rank_color}99 100%); 
                        padding: 1.5rem; border-radius: 1rem; color: white;">
                <h2 style="margin: 0; color: white;">{selected_customer['氏名']}</h2>
                <p style="margin: 0.5rem 0; opacity: 0.9;">ID: {selected_customer['顧客ID']}</p>
                <p style="margin: 0; font-size: 1.2rem;">
                    <span style="background: rgba(255,255,255,0.2); padding: 0.25rem 0.75rem; border-radius: 1rem;">
                        {selected_customer['会員ランク']}会員
                    </span>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📋 顧客情報")
            st.markdown(f"""
            <div class="metric-box">
                <p style="margin: 0; color: #718096; font-size: 0.8rem;">累計LTV</p>
                <p style="margin: 0; font-size: 1.5rem; font-weight: bold; color: #1a365d;">¥{selected_customer['LTV']:,}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**📧 メール:** {selected_customer['メールアドレス']}")
            st.markdown(f"**📞 電話:** {selected_customer['電話番号']}")
            st.markdown(f"**📍 住所:** {selected_customer['住所']}")
            st.markdown(f"**📅 最終買取日:** {selected_customer['最終買取日']}")
            st.markdown(f"**🎂 登録日:** {selected_customer['登録日']}")
        
        with col2:
            # 対応履歴
            st.markdown("### 📝 対応履歴")
            customer_interactions = interactions[interactions['顧客ID'] == selected_customer['顧客ID']]
            
            if len(customer_interactions) > 0:
                for _, row in customer_interactions.iterrows():
                    status_color = "#38a169" if row['ステータス'] == '完了' else "#dd6b20"
                    type_emoji = {
                        '買取': '📦',
                        '問合せ': '❓',
                        'クレーム': '⚠️',
                        'VIP対応': '👑'
                    }.get(row['対応種別'], '📌')
                    
                    st.markdown(f"""
                    <div class="interaction-item">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span><strong>{type_emoji} {row['対応種別']}</strong> - {row['対応日時']}</span>
                            <span style="background: {status_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 0.25rem; font-size: 0.75rem;">
                                {row['ステータス']}
                            </span>
                        </div>
                        <p style="margin: 0.5rem 0 0 0; color: #4a5568;">担当: {row['担当者']} | {row['内容']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("対応履歴がありません")
            
            # 担当者メモ
            st.markdown("### ✏️ 担当者メモ")
            
            memos = load_memos()
            customer_memos = memos[memos['顧客ID'] == selected_customer['顧客ID']]
            
            if len(customer_memos) > 0:
                for _, memo in customer_memos.iterrows():
                    st.markdown(f"""
                    <div style="background: #fffbeb; padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border-left: 3px solid #f59e0b;">
                        <small style="color: #92400e;">{memo['メモ日時']} - {memo['担当者']}</small>
                        <p style="margin: 0.25rem 0 0 0;">{memo['メモ内容']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # メモ追加フォーム
            with st.form("memo_form"):
                col_a, col_b = st.columns([1, 3])
                with col_a:
                    author = st.text_input("担当者名", placeholder="山田")
                with col_b:
                    memo_content = st.text_area("メモ内容", placeholder="次回の買取で注意すべき点など...", height=80)
                
                if st.form_submit_button("📌 メモを追加", type="primary"):
                    if author and memo_content:
                        save_memo(selected_customer['顧客ID'], author, memo_content)
                        st.success("メモを保存しました！")
                        st.rerun()
                    else:
                        st.warning("担当者名とメモ内容を入力してください")
    
    else:
        # 顧客一覧表示
        st.markdown("### 📋 顧客一覧")
        st.markdown("サイドバーから顧客を検索してください")
        
        # ランク別集計
        rank_counts = customers['会員ランク'].value_counts()
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👑 プラチナ", f"{rank_counts.get('プラチナ', 0)}名")
        with col2:
            st.metric("🥇 ゴールド", f"{rank_counts.get('ゴールド', 0)}名")
        with col3:
            st.metric("🥈 シルバー", f"{rank_counts.get('シルバー', 0)}名")
        with col4:
            st.metric("🥉 ブロンズ", f"{rank_counts.get('ブロンズ', 0)}名")
        
        st.dataframe(
            customers[['顧客ID', '氏名', '会員ランク', 'LTV', '最終買取日']],
            use_container_width=True,
            hide_index=True
        )

if __name__ == "__main__":
    main()



