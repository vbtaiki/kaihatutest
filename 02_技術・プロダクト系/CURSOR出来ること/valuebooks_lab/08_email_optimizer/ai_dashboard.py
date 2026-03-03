"""
バリューブックス AIメール生成ダッシュボード
顧客を選択してボタンを押すとGPT-4でメールを生成

使い方:
  export OPENAI_API_KEY="sk-..."
  streamlit run 08_email_optimizer/ai_dashboard.py
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from openai import OpenAI

# ページ設定
st.set_page_config(
    page_title="AIメール生成",
    page_icon="🤖",
    layout="wide"
)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a5f;
        margin-bottom: 1rem;
    }
    .customer-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1rem;
    }
    .email-preview {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .email-subject {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e3a5f;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 0.75rem;
        margin-bottom: 1rem;
    }
    .email-body {
        font-size: 0.95rem;
        line-height: 1.8;
        color: #334155;
        white-space: pre-wrap;
    }
    .generating {
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        background-size: 200% 100%;
        animation: gradient 2s ease infinite;
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .type-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .type-urgent { background: #fef2f2; color: #dc2626; }
    .type-normal { background: #fffbeb; color: #d97706; }
    .type-purchase { background: #f0fdf4; color: #16a34a; }
    .type-news { background: #eff6ff; color: #2563eb; }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'generated_email' not in st.session_state:
    st.session_state.generated_email = None
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False

def load_all_data():
    """全データを読み込む"""
    data = {}
    
    warehouse_path = os.path.join(DATA_DIR, 'warehouse_status.json')
    if os.path.exists(warehouse_path):
        with open(warehouse_path, 'r', encoding='utf-8') as f:
            data['warehouse'] = json.load(f)
    
    customers_path = os.path.join(DATA_DIR, 'customers_full.csv')
    if os.path.exists(customers_path):
        data['customers'] = pd.read_csv(customers_path)
    else:
        customers_path = os.path.join(DATA_DIR, 'customers_email.csv')
        if os.path.exists(customers_path):
            data['customers'] = pd.read_csv(customers_path)
    
    news_path = os.path.join(DATA_DIR, 'recent_news.json')
    if os.path.exists(news_path):
        with open(news_path, 'r', encoding='utf-8') as f:
            data['news'] = json.load(f).get('news_items', [])
    
    return data

def analyze_slack_periods(warehouse):
    """閑散期を分析"""
    forecast = warehouse.get('weekly_forecast', [])
    threshold = warehouse.get('thresholds', {}).get('閑散期_capacity_under', 0.45)
    return [d['date'] for d in forecast if d['capacity_usage'] < threshold]

def determine_email_type(customer, warehouse, today):
    """メールタイプを判定"""
    last_email = datetime.strptime(customer['最終メール送信日'], '%Y-%m-%d')
    days_since = (today - last_email).days
    
    slack_days = analyze_slack_periods(warehouse)
    backlog = warehouse.get('backlog', {}).get('未査定_箱数', 150)
    activity = customer.get('購入傾向', '買取メイン')
    
    urgency = "高" if backlog < 100 and len(slack_days) >= 3 else "中" if len(slack_days) >= 1 else "低"
    
    if days_since < 7:
        return None, "送信間隔が短すぎる（7日未満）", "skip"
    elif days_since < 14 and urgency != "高":
        return None, "もう少し間隔を空ける（14日未満）", "skip"
    elif urgency == "高" and activity in ['買取メイン', '両方活発']:
        return "緊急買取促進", f"閑散期{len(slack_days)}日間・緊急度高", "urgent"
    elif len(slack_days) > 0 and activity == '買取メイン':
        return "通常買取促進", "閑散期のため買取促進", "normal"
    elif activity == '購入メイン':
        return "購入促進", "購入傾向の顧客", "purchase"
    else:
        return "ニュース", "関係構築", "news"

def build_prompt(customer, email_type, reason, warehouse, news):
    """LLMプロンプトを構築"""
    slack_days = analyze_slack_periods(warehouse)
    backlog = warehouse.get('backlog', {})
    
    genre = customer.get('得意ジャンル', '')
    matching_news = [n for n in news if any(g in genre for g in n.get('related_genres', [])) or '全ジャンル' in n.get('related_genres', [])]
    
    news_text = ""
    if matching_news:
        news_text = "\n## 関連ニュース\n" + "\n".join([f"- {n['title']}: {n['summary']}" for n in matching_news[:2]])
    
    prompt = f"""あなたはバリューブックスのメールライターです。
以下の状況を総合的に判断し、最適なメールを作成してください。

## 送信判断
- 推奨メールタイプ: {email_type}
- 判断理由: {reason}

## 顧客情報
- 氏名: {customer['氏名']}
- 会員ランク: {customer['会員ランク']}
- 傾向: {customer.get('購入傾向', 'N/A')}
- 得意ジャンル: {customer.get('得意ジャンル', 'N/A')}
- 累計買取: {customer.get('累計買取回数', 0)}回 / ¥{customer.get('累計買取金額', 0):,}
- 累計購入: {customer.get('累計購入回数', 0)}回 / ¥{customer.get('累計購入金額', 0):,}

## 倉庫状況
- 閑散期: {len(slack_days)}日間（20%UPキャンペーン実施中）
- 未査定バックログ: {backlog.get('未査定_箱数', 0)}箱
{news_text}

## メール種別ごとのトーン
- 緊急買取促進: 「本日限定！」など緊急感を出す
- 通常買取促進: 「そろそろ本の整理はいかがですか？」など自然なトーン
- 購入促進: おすすめ本を提案
- ニュース: 情報提供メイン

## 作成条件
1. 件名は20文字以内
2. 本文は150〜200文字
3. 顧客の名前を使ってパーソナライズ
4. 得意ジャンルに言及する
5. 押し売り感を出さない

## 出力形式（これに従ってください）
件名: [件名をここに]

本文:
[本文をここに]"""
    
    return prompt

def generate_email_with_gpt(prompt):
    """GPT-4でメールを生成"""
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは古書店バリューブックスのプロのメールライターです。顧客に寄り添った、温かみのあるメールを書きます。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, str(e)

def parse_email_response(response):
    """GPTの出力をパース"""
    lines = response.strip().split('\n')
    subject = ""
    body_lines = []
    in_body = False
    
    for line in lines:
        if line.startswith('件名:') or line.startswith('件名：'):
            subject = line.replace('件名:', '').replace('件名：', '').strip()
        elif line.startswith('本文:') or line.startswith('本文：'):
            in_body = True
        elif in_body:
            body_lines.append(line)
    
    return subject, '\n'.join(body_lines).strip()

def main():
    st.markdown('<p class="main-header">🤖 AIメール生成ダッシュボード</p>', unsafe_allow_html=True)
    
    # APIキー確認
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        st.error("⚠️ OPENAI_API_KEY が設定されていません。ターミナルで `export OPENAI_API_KEY='sk-...'` を実行してから起動してください。")
        return
    
    st.success(f"✅ APIキー確認OK: {api_key[:15]}...")
    
    data = load_all_data()
    today = datetime.now()
    
    if 'warehouse' not in data or 'customers' not in data:
        st.error("データが見つかりません")
        return
    
    warehouse = data['warehouse']
    customers = data['customers']
    news = data.get('news', [])
    
    # 閑散期情報
    slack_days = analyze_slack_periods(warehouse)
    if slack_days:
        st.warning(f"⚠️ 閑散期検出: {len(slack_days)}日間（20%UPキャンペーン推奨）")
    
    st.markdown("---")
    
    # 2カラムレイアウト
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 👤 顧客を選択")
        
        # 顧客リストを作成（送信対象のみ）
        customer_list = []
        for _, c in customers.iterrows():
            email_type, reason, type_class = determine_email_type(c, warehouse, today)
            if email_type:
                customer_list.append({
                    'customer': c,
                    'email_type': email_type,
                    'reason': reason,
                    'type_class': type_class
                })
        
        if not customer_list:
            st.info("送信対象の顧客がいません")
            return
        
        # 顧客選択
        customer_options = [f"{item['customer']['氏名']}（{item['customer']['会員ランク']}）" for item in customer_list]
        selected_idx = st.selectbox("顧客", range(len(customer_list)), format_func=lambda x: customer_options[x])
        
        selected = customer_list[selected_idx]
        c = selected['customer']
        
        # 顧客情報カード
        st.markdown(f"""
        <div class="customer-card">
            <h3 style="margin:0; color:white;">{c['氏名']}</h3>
            <p style="margin:0.5rem 0; opacity:0.9;">{c['会員ランク']}会員</p>
            <p style="margin:0; font-size:0.9rem;">📚 {c.get('得意ジャンル', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 詳細情報
        st.markdown("**📊 顧客データ**")
        st.markdown(f"- 累計買取: {c.get('累計買取回数', 0)}回")
        st.markdown(f"- 累計購入: {c.get('累計購入回数', 0)}回")
        st.markdown(f"- 傾向: {c.get('購入傾向', 'N/A')}")
        
        st.markdown("---")
        
        # メールタイプ
        type_badge_class = f"type-{selected['type_class']}"
        st.markdown(f"""
        <div>
            <span class="type-badge {type_badge_class}">{selected['email_type']}</span>
        </div>
        <p style="font-size:0.85rem; color:#64748b; margin-top:0.5rem;">{selected['reason']}</p>
        """, unsafe_allow_html=True)
        
        # 生成ボタン
        st.markdown("---")
        if st.button("🤖 メールを生成", type="primary", use_container_width=True):
            st.session_state.is_generating = True
            st.session_state.generated_email = None
            
            # プロンプト構築
            prompt = build_prompt(c, selected['email_type'], selected['reason'], warehouse, news)
            
            # 生成
            with st.spinner("GPT-4で生成中..."):
                response, error = generate_email_with_gpt(prompt)
            
            if error:
                st.error(f"エラー: {error}")
                st.session_state.is_generating = False
            else:
                subject, body = parse_email_response(response)
                st.session_state.generated_email = {
                    'to': c['メールアドレス'],
                    'subject': subject,
                    'body': body,
                    'customer_name': c['氏名'],
                    'type': selected['email_type']
                }
                st.session_state.is_generating = False
                st.rerun()
    
    with col2:
        st.markdown("### ✉️ 生成されたメール")
        
        if st.session_state.generated_email:
            email = st.session_state.generated_email
            
            st.markdown(f"""
            <div class="email-preview">
                <div style="color:#64748b; font-size:0.85rem; margin-bottom:0.5rem;">
                    To: {email['to']}
                </div>
                <div class="email-subject">
                    📧 {email['subject']}
                </div>
                <div class="email-body">
{email['body']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # アクションボタン
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("📋 コピー", use_container_width=True):
                    st.code(f"件名: {email['subject']}\n\n{email['body']}")
            
            with col_b:
                if st.button("🔄 再生成", use_container_width=True):
                    st.session_state.generated_email = None
                    st.rerun()
            
            with col_c:
                if st.button("✅ 送信済みにする", use_container_width=True):
                    st.success(f"✅ {email['customer_name']}様へのメールを送信済みにしました")
        
        else:
            st.markdown("""
            <div style="background:#f8fafc; padding:3rem; border-radius:1rem; text-align:center; color:#94a3b8;">
                <div style="font-size:3rem; margin-bottom:1rem;">📧</div>
                <p>左のパネルで顧客を選択し、</p>
                <p><strong>「🤖 メールを生成」</strong>ボタンを押してください</p>
            </div>
            """, unsafe_allow_html=True)
        
        # プロンプト表示
        with st.expander("🔍 LLMに送信したプロンプトを確認"):
            c = customer_list[selected_idx]['customer']
            prompt = build_prompt(c, selected['email_type'], selected['reason'], warehouse, news)
            st.code(prompt, language="markdown")

if __name__ == "__main__":
    main()



