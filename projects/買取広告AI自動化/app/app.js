'use strict';

/* ================================
   状態管理
================================ */
const State = {
  activeTab: 'dashboard',
  budgetAllocations: {
    Google: 70,
    Meta: 55,
    LINE: 25,
    YDA: 15,
    チラシ: 15,
  },
  totalBudget: 180,
  targetAcquisitions: 1200,
  targetCPA: 2000,
  queueItems: [],
  competePairs: [],
  allCreatives: [],
  generatedCreatives: [],
};

/* ================================
   モックデータ
================================ */
const CREATIVES = [
  { id: 1, name: '今なら査定額+10%キャンペーン', media: 'Meta', appeal: 'お得感', ctr: 3.8, cvr: 3.2, cpa: 1480, views: 142000, generator: 'AI', emoji: '💰' },
  { id: 2, name: '30秒で申込完了！', media: 'Google', appeal: '簡単', ctr: 3.1, cvr: 2.9, cpa: 1620, views: 98000, generator: 'AI', emoji: '⚡' },
  { id: 3, name: '累計500万冊の買取実績', media: 'Google', appeal: '信頼', ctr: 2.4, cvr: 2.5, cpa: 1740, views: 115000, generator: '人間', emoji: '📊' },
  { id: 4, name: 'スマホで写真を撮るだけ', media: 'Meta', appeal: '簡単', ctr: 2.9, cvr: 2.8, cpa: 1680, views: 88000, generator: 'AI', emoji: '📱' },
  { id: 5, name: '本棚がスッキリ！お金ももらえる', media: 'LINE', appeal: 'お得感', ctr: 2.6, cvr: 2.4, cpa: 1890, views: 72000, generator: 'AI', emoji: '✨' },
  { id: 6, name: '最短翌日に集荷に来ます', media: 'Google', appeal: 'スピード', ctr: 2.3, cvr: 2.2, cpa: 1980, views: 64000, generator: 'AI', emoji: '🚚' },
  { id: 7, name: '春の大掃除で稼ごう', media: 'Meta', appeal: 'お得感', ctr: 2.1, cvr: 2.0, cpa: 2100, views: 58000, generator: '人間', emoji: '🌸' },
  { id: 8, name: '査定額に自信あり！他社と比較を', media: 'YDA', appeal: '信頼', ctr: 1.8, cvr: 1.9, cpa: 2240, views: 45000, generator: '人間', emoji: '🏆' },
  { id: 9, name: '引越し前に本を処分しよう', media: 'LINE', appeal: '簡単', ctr: 1.6, cvr: 1.7, cpa: 2380, views: 39000, generator: 'AI', emoji: '🏠' },
  { id: 10, name: 'チラシ：買取額+5%クーポン', media: 'チラシ', appeal: 'お得感', ctr: null, cvr: 4.2, cpa: 1250, views: 30000, generator: '人間', emoji: '📮' },
  { id: 11, name: '初めてでも安心！丁寧な対応', media: 'YDA', appeal: '信頼', ctr: 1.4, cvr: 1.5, cpa: 2440, views: 35000, generator: 'AI', emoji: '🤝' },
  { id: 12, name: '本を売ろう', media: 'Google', appeal: 'お得感', ctr: 0.4, cvr: 0.9, cpa: 3200, views: 28000, generator: 'AI', emoji: '📚' },
];

const COMPETE_PAIRS = [
  {
    id: 1,
    theme: 'Google Ads バナー 300x250 — 5月第2週',
    media: 'Google',
    status: 'running',
    human: {
      name: '手書きPOP風 春の大掃除', emoji: '🌸',
      copy: '春の大掃除で眠ってる本を売ろう！査定無料、送料ゼロ。',
      scores: { ctr: 2.1, cvr: 1.8, cpa: 2200 },
      bgGrad: 'linear-gradient(135deg, #fff8e1, #ffecb3)',
    },
    ai: {
      name: 'お得感訴求 損失回避型', emoji: '💰',
      copy: '今なら査定額+10%！この本、まだお金に変えてないんですか？',
      scores: { ctr: 3.6, cvr: 3.0, cpa: 1550 },
      bgGrad: 'linear-gradient(135deg, #e0f7fa, #b2ebf2)',
    },
    winner: 'ai',
  },
  {
    id: 2,
    theme: 'Meta Ads フィード — 5月第1週',
    media: 'Meta',
    status: 'completed',
    human: {
      name: '季節訴求 GW断捨離', emoji: '🎏',
      copy: 'GWに断捨離！本を売ってスッキリ&現金ゲット。',
      scores: { ctr: 3.2, cvr: 2.9, cpa: 1680 },
      bgGrad: 'linear-gradient(135deg, #fce4ec, #f8bbd0)',
    },
    ai: {
      name: 'スピード訴求 AI最適化', emoji: '⚡',
      copy: '申込から集荷まで最短48時間。本をすぐ現金化できます。',
      scores: { ctr: 2.7, cvr: 2.5, cpa: 1820 },
      bgGrad: 'linear-gradient(135deg, #e8f5e9, #c8e6c9)',
    },
    winner: 'human',
  },
  {
    id: 3,
    theme: 'LINE Ads バナー — 4月第4週',
    media: 'LINE',
    status: 'completed',
    human: {
      name: '信頼訴求 実績強調', emoji: '📊',
      copy: '累計500万冊の買取実績。バリューブックスなら安心です。',
      scores: { ctr: 1.9, cvr: 2.1, cpa: 2100 },
      bgGrad: 'linear-gradient(135deg, #e8eaf6, #c5cae9)',
    },
    ai: {
      name: 'お得感訴求 数字強調', emoji: '💰',
      copy: '本1冊で最大〇〇円！まず無料査定してみませんか？',
      scores: { ctr: 2.5, cvr: 2.8, cpa: 1750 },
      bgGrad: 'linear-gradient(135deg, #fff3e0, #ffe0b2)',
    },
    winner: 'ai',
  },
];

const QUEUE_ITEMS = [
  { id: 1, name: 'Google_お得感_バナー300x250_0501', media: 'Google', size: '300x250', appeal: 'お得感', status: 'pending', emoji: '💰', generator: 'AI', createdAt: '5/1 14:32', cpaEst: 1520 },
  { id: 2, name: 'Meta_簡単訴求_フィード_0501', media: 'Meta', size: '1080x1080', appeal: '簡単', status: 'pending', emoji: '📱', generator: 'AI', createdAt: '5/1 14:32', cpaEst: 1680 },
  { id: 3, name: 'LINE_スピード_バナー728x90_0430', media: 'LINE', size: '728x90', appeal: 'スピード', status: 'approved', emoji: '⚡', generator: 'AI', createdAt: '4/30 11:10', cpaEst: 1950 },
  { id: 4, name: '春のPOP風_Meta_人間制作_0429', media: 'Meta', size: '1080x1080', appeal: '季節感', status: 'pending', emoji: '🌸', generator: '人間', createdAt: '4/29 16:05', cpaEst: 1680 },
  { id: 5, name: 'Google_信頼訴求_バナー_0428', media: 'Google', size: '336x280', appeal: '信頼', status: 'pending', emoji: '🛡️', generator: 'AI', createdAt: '4/28 09:40', cpaEst: 1740 },
  { id: 6, name: 'YDA_お得感_0427', media: 'YDA', size: '336x280', appeal: 'お得感', status: 'rejected', emoji: '⚠️', generator: 'AI', createdAt: '4/27 15:00', cpaEst: 2440 },
  { id: 7, name: 'Meta_損失回避_0425', media: 'Meta', size: '1080x1080', appeal: 'お得感', status: 'submitted', emoji: '💰', generator: 'AI', createdAt: '4/25 10:20', cpaEst: 1480 },
  { id: 8, name: 'Google_スピード_バナー_0424', media: 'Google', size: '300x250', appeal: 'スピード', status: 'submitted', emoji: '🚚', generator: 'AI', createdAt: '4/24 08:55', cpaEst: 1620 },
  { id: 9, name: 'LINE_信頼訴求_0424', media: 'LINE', size: '728x90', appeal: '信頼', status: 'approved', emoji: '🤝', generator: '人間', createdAt: '4/24 08:55', cpaEst: 1890 },
  { id: 10, name: 'チラシ_GWキャンペーン_0420', media: 'チラシ', size: 'A4縦', appeal: 'お得感', status: 'submitted', emoji: '📮', generator: '人間', createdAt: '4/20 13:30', cpaEst: 1250 },
];

const GENERATED_TEMPLATES = [
  { emoji: '💰', copy: '今なら査定額+10%！本がお金になります。', hook: 'お得感' },
  { emoji: '📦', copy: '段ボールに詰めて送るだけ。送料無料で査定します。', hook: '簡単' },
  { emoji: '⚡', copy: '最短翌日集荷。読み終わった本をすぐ現金化。', hook: 'スピード' },
  { emoji: '🛡️', copy: '累計500万冊・利用者35万人の実績。安心の買取。', hook: '信頼' },
  { emoji: '😮', copy: 'その本、まだ売ってないんですか？今が一番高い。', hook: '驚き' },
  { emoji: '📚', copy: '本棚がスッキリ。お金ももらえる。一石二鳥の買取。', hook: '簡単' },
  { emoji: '🏠', copy: '引越し前に本を処分。査定無料、自宅まで集荷します。', hook: '簡単' },
  { emoji: '🌟', copy: '今月限定！買取金額に+5%上乗せキャンペーン実施中。', hook: 'お得感' },
];

/* ================================
   タブ切り替え
================================ */
function switchTab(tabName) {
  State.activeTab = tabName;
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(`tab-${tabName}`).classList.add('active');
  const btns = document.querySelectorAll('.tab-btn');
  const tabOrder = ['dashboard', 'plan', 'analysis', 'generate', 'compete', 'queue'];
  const idx = tabOrder.indexOf(tabName);
  if (idx >= 0) btns[idx].classList.add('active');
}

/* ================================
   日付表示
================================ */
function initDate() {
  const el = document.getElementById('now-date');
  if (!el) return;
  const now = new Date();
  el.textContent = now.toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric' });
}

/* ================================
   トースト通知
================================ */
function showToast(message, type = 'success', duration = 3500) {
  const container = document.getElementById('toast-container');
  const icons = { success: '✅', info: 'ℹ️', warning: '⚠️' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${icons[type] || '✅'}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('removing');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

/* ================================
   ダッシュボード: トレンドチャート
================================ */
function renderTrendChart() {
  const data = [
    { label: '月', val: 98 },
    { label: '火', val: 112 },
    { label: '水', val: 105 },
    { label: '木', val: 118 },
    { label: '金', val: 132 },
    { label: '土', val: 178 },
    { label: '日', val: 165 },
  ];
  const max = Math.max(...data.map(d => d.val));
  const container = document.getElementById('trend-chart');
  if (!container) return;
  container.innerHTML = data.map(d => `
    <div class="bar-col">
      <div class="bar-val">${d.val}</div>
      <div class="bar-fill${d.label === '土' || d.label === '日' ? ' accent' : ''}" style="height:${Math.round((d.val / max) * 90)}px;"></div>
      <div class="bar-label">${d.label}</div>
    </div>
  `).join('');
}

/* ================================
   ダッシュボード: トップ3クリエイティブ
================================ */
function renderTopCreativesDashboard() {
  const top3 = [...CREATIVES].sort((a, b) => a.cpa - b.cpa).slice(0, 3);
  const container = document.getElementById('top-creatives-dashboard');
  if (!container) return;
  container.innerHTML = top3.map((c, i) => {
    const ranks = ['gold', 'silver', ''];
    const rankLabels = ['🥇 1位', '🥈 2位', '🥉 3位'];
    return `
    <div class="creative-card">
      <div class="creative-thumbnail" style="background:linear-gradient(135deg,#e0f7fa,#b2dfdb);">
        <span style="font-size:52px;">${c.emoji}</span>
        <div class="creative-text">${c.appeal}訴求 / ${c.media}</div>
      </div>
      <div class="creative-rank ${ranks[i]}">${rankLabels[i]}</div>
      <div class="creative-meta">
        <div class="creative-name">${c.name}</div>
        <div class="metrics-row">
          ${c.ctr ? `<span class="metric-chip ctr">CTR ${c.ctr}%</span>` : ''}
          <span class="metric-chip cvr">CVR ${c.cvr}%</span>
          <span class="metric-chip cpa">CPA ¥${c.cpa.toLocaleString()}</span>
        </div>
        <div style="font-size:11px;color:var(--text-secondary);">${c.generator} 制作 / ${c.media}</div>
      </div>
      <div class="creative-actions">
        <button class="btn btn-outline btn-sm" onclick="addToQueue(${c.id})">📬 入稿キューへ</button>
        <button class="btn btn-ghost btn-sm" onclick="seedGenerate(${c.id})">✨ これをシードに生成</button>
      </div>
    </div>
    `;
  }).join('');
}

/* ================================
   予算配分プラン
================================ */
const MEDIA_META = {
  Google:  { badge: 'google',  emoji: '🔵', cpaBase: 1520, reason: '検索意図が強く、CPA実績が安定。高い配分を推奨。' },
  Meta:    { badge: 'meta',    emoji: '🟣', cpaBase: 1680, reason: '「お得感」訴求の相性が良く、CVR改善中。強化推奨。' },
  LINE:    { badge: 'line',    emoji: '🟢', cpaBase: 2100, reason: 'リーチ効率は良いがCPAが目標付近。様子見で維持。' },
  YDA:    { badge: 'yda',     emoji: '🟡', cpaBase: 2440, reason: 'CPA目標超過中。配分を減らし改善後に再増配を推奨。' },
  チラシ: { badge: 'flyer',   emoji: '📮', cpaBase: 1250, reason: '配信済み。次回分の原稿生成を準備中。' },
};

function renderBudgetSliders() {
  const container = document.getElementById('budget-sliders');
  if (!container) return;
  const total = State.totalBudget;
  container.innerHTML = Object.entries(State.budgetAllocations).map(([media, val]) => {
    const pct = Math.round((val / total) * 100);
    const m = MEDIA_META[media];
    return `
    <div style="margin-bottom:16px;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
        <span class="media-badge ${m.badge}">${m.emoji} ${media}</span>
        <span style="font-size:12px;color:var(--text-secondary);">${pct}%</span>
      </div>
      <div class="slider-wrap">
        <input type="range" min="0" max="${total}" value="${val}" step="1"
          oninput="updateAllocation('${media}', this.value)"
          id="slider-${media}">
        <span class="slider-value" id="val-${media}">¥${val}万</span>
      </div>
    </div>`;
  }).join('');
}

function updateAllocation(media, value) {
  State.budgetAllocations[media] = parseInt(value);
  document.getElementById(`val-${media}`).textContent = `¥${value}万`;
  const newTotal = Object.values(State.budgetAllocations).reduce((a, b) => a + b, 0);
  document.getElementById('plan-total-label').textContent = `合計: ¥${newTotal}万`;
  renderPlanTable();
}

function renderPlanTable() {
  const tbody = document.getElementById('plan-table-body');
  if (!tbody) return;
  const total = Object.values(State.budgetAllocations).reduce((a, b) => a + b, 0);
  tbody.innerHTML = Object.entries(State.budgetAllocations).map(([media, budget]) => {
    const m = MEDIA_META[media];
    const pct = total > 0 ? Math.round((budget / total) * 100) : 0;
    const estCpa = m.cpaBase;
    const estAcq = budget > 0 ? Math.round((budget * 10000) / estCpa) : 0;
    return `
    <tr>
      <td><span class="media-badge ${m.badge}">${m.emoji} ${media}</span></td>
      <td><strong>¥${budget}万</strong></td>
      <td>${pct}%</td>
      <td><strong>${estAcq.toLocaleString()}件</strong></td>
      <td>¥${estCpa.toLocaleString()}</td>
      <td style="font-size:12px;color:var(--text-secondary);max-width:240px;">${m.reason}</td>
    </tr>`;
  }).join('');
}

function recalcBudget() {
  const budget = parseFloat(document.getElementById('total-budget')?.value) || 180;
  State.totalBudget = budget;
  State.targetAcquisitions = parseInt(document.getElementById('target-acquisitions')?.value) || 1200;
  State.targetCPA = parseInt(document.getElementById('target-cpa')?.value) || 2000;
}

function runAIPlanCalc() {
  showToast('AIが過去データを分析し最適配分を算出しています...', 'info', 2000);
  const total = State.totalBudget;
  setTimeout(() => {
    State.budgetAllocations = {
      Google: Math.round(total * 0.38),
      Meta:   Math.round(total * 0.30),
      LINE:   Math.round(total * 0.14),
      YDA:    Math.round(total * 0.08),
      チラシ: Math.round(total * 0.10),
    };
    renderBudgetSliders();
    renderPlanTable();
    showToast('AIが最適配分を算出しました。スライダーで調整できます。', 'success');
  }, 1800);
}

function approveAndSubmitPlan() {
  showToast('配分計画を確定しました。入稿キューに追加します。', 'success');
  setTimeout(() => switchTab('queue'), 1200);
}

/* ================================
   クリエイティブ分析
================================ */
function renderCreativeGrid(list) {
  const container = document.getElementById('creative-grid');
  if (!container) return;
  if (list.length === 0) {
    container.innerHTML = '<div class="empty-state" style="grid-column:1/-1;"><div class="empty-state-icon">🔍</div><div class="empty-state-title">条件に合うクリエイティブが見つかりません</div></div>';
    return;
  }
  container.innerHTML = list.map(c => `
    <div class="creative-card">
      <div class="creative-thumbnail" style="background:linear-gradient(135deg,#e0f7fa,#b2dfdb);">
        <span style="font-size:52px;">${c.emoji}</span>
        <div class="creative-text">${c.appeal}訴求 / ${c.media}</div>
      </div>
      ${c.cpa < 1700 ? '<div class="winner-badge">🏆 勝ちクリエイティブ</div>' : ''}
      <div class="creative-meta">
        <div class="creative-name">${c.name}</div>
        <div class="metrics-row">
          ${c.ctr ? `<span class="metric-chip ctr">CTR ${c.ctr}%</span>` : '<span class="metric-chip ctr">CTR —</span>'}
          <span class="metric-chip cvr">CVR ${c.cvr}%</span>
          <span class="metric-chip cpa">CPA ¥${c.cpa.toLocaleString()}</span>
        </div>
        <div style="font-size:11px;color:var(--text-secondary);">${c.generator} 制作 / 表示 ${c.views.toLocaleString()}回</div>
      </div>
      <div class="creative-actions">
        <button class="btn btn-outline btn-sm" onclick="addToQueue(${c.id})">📬 入稿へ</button>
        <button class="btn btn-ghost btn-sm" onclick="seedGenerate(${c.id})">✨ シード生成</button>
      </div>
    </div>
  `).join('');
}

function filterCreatives() {
  const media = document.getElementById('filter-media')?.value;
  const appeal = document.getElementById('filter-appeal')?.value;
  const sort = document.getElementById('sort-creatives')?.value;
  let list = [...CREATIVES];
  if (media !== 'all') list = list.filter(c => c.media === media);
  if (appeal !== 'all') list = list.filter(c => c.appeal === appeal);
  if (sort === 'cpa') list.sort((a, b) => a.cpa - b.cpa);
  else if (sort === 'cvr') list.sort((a, b) => b.cvr - a.cvr);
  else if (sort === 'ctr') list.sort((a, b) => (b.ctr || 0) - (a.ctr || 0));
  renderCreativeGrid(list);
}

function addToQueue(id) {
  showToast('入稿キューに追加しました。', 'success');
  const qCount = document.getElementById('q-pending-count');
  if (qCount) qCount.textContent = parseInt(qCount.textContent) + 1;
}

function seedGenerate(id) {
  const c = CREATIVES.find(x => x.id === id);
  if (c) showToast(`「${c.name}」をシードに新しいクリエイティブを生成します。`, 'info');
  setTimeout(() => switchTab('generate'), 1000);
}

/* ================================
   クリエイティブ生成
================================ */
function toggleChip(el) {
  el.classList.toggle('selected');
}

function generateCreatives() {
  const count = parseInt(document.getElementById('gen-count')?.value) || 5;
  const media = document.getElementById('gen-media')?.value;
  const instruction = document.getElementById('gen-instruction')?.value;
  const selectedAppeals = [...document.querySelectorAll('#appeal-chips .chip.selected')].map(c => c.dataset.appeal);
  const selectedTargets = [...document.querySelectorAll('#target-chips .chip.selected')].map(c => c.dataset.target);

  const resultArea = document.getElementById('generate-result-area');
  resultArea.innerHTML = `
    <div style="text-align:center;padding:48px;background:var(--surface);border-radius:var(--radius);box-shadow:var(--shadow);">
      <div style="font-size:32px;margin-bottom:12px;">🤖</div>
      <div style="font-weight:700;margin-bottom:8px;">AIがクリエイティブを生成しています...</div>
      <div class="loading-dots"><span></span><span></span><span></span></div>
      <div style="font-size:12px;color:var(--text-secondary);margin-top:10px;">${media}向け ${count}案を生成中</div>
    </div>`;

  setTimeout(() => {
    const templates = [...GENERATED_TEMPLATES].sort(() => Math.random() - 0.5).slice(0, count);
    const cards = templates.map((t, i) => {
      const cpaEst = 1400 + Math.floor(Math.random() * 600);
      const ctrEst = (1.8 + Math.random() * 2.2).toFixed(1);
      const cvrEst = (1.5 + Math.random() * 2.0).toFixed(1);
      return `
      <div class="creative-card" style="margin-bottom:14px;">
        <div class="creative-thumbnail" style="background:linear-gradient(135deg,${randomGrad()});">
          <span style="font-size:52px;">${t.emoji}</span>
          <div class="creative-text">${t.hook}訴求 / ${media}</div>
        </div>
        <div class="creative-rank">AI 生成案${i + 1}</div>
        <div class="creative-meta">
          <div class="creative-name" style="white-space:normal;font-size:13px;line-height:1.5;">${t.copy}</div>
          ${instruction ? `<div style="font-size:11px;color:var(--primary-dark);margin-top:4px;padding:4px 8px;background:var(--primary-light);border-radius:4px;">📝 指示反映済み</div>` : ''}
          <div class="metrics-row" style="margin-top:8px;">
            <span class="metric-chip ctr">予測 CTR ${ctrEst}%</span>
            <span class="metric-chip cvr">予測 CVR ${cvrEst}%</span>
            <span class="metric-chip cpa">予測 CPA ¥${cpaEst.toLocaleString()}</span>
          </div>
        </div>
        <div class="creative-actions">
          <button class="btn btn-primary btn-sm" onclick="sendToQueue(this, '${t.hook}訴求_${media}_AI生成案${i+1}', '${media}')">📬 入稿キューへ</button>
          <button class="btn btn-ghost btn-sm" onclick="sendToCompete(this, '${t.hook}訴求_AI生成案${i+1}')">⚔️ コンペへ</button>
        </div>
      </div>`;
    });

    resultArea.innerHTML = `
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
        <div style="font-weight:700;font-size:15px;">${count}案を生成しました</div>
        <button class="btn btn-accent btn-sm" onclick="sendAllToQueue()">📬 全案を入稿キューへ</button>
      </div>
      ${cards.join('')}`;

    showToast(`${count}案のクリエイティブを生成しました！`, 'success');
  }, 2200);
}

function randomGrad() {
  const grads = [
    '#e0f7fa,#b2ebf2', '#e8f5e9,#c8e6c9', '#fff3e0,#ffe0b2',
    '#fce4ec,#f8bbd0', '#ede7f6,#d1c4e9', '#e3f2fd,#bbdefb',
  ];
  return grads[Math.floor(Math.random() * grads.length)];
}

function sendToQueue(btn, name, media) {
  btn.disabled = true;
  btn.textContent = '✅ 追加済み';
  const qCount = document.getElementById('q-pending-count');
  if (qCount) qCount.textContent = parseInt(qCount.textContent) + 1;
  showToast(`「${name}」を入稿キューに追加しました。`, 'success');
}

function sendToCompete(btn, name) {
  btn.disabled = true;
  btn.textContent = '⚔️ 参戦済み';
  showToast(`「${name}」をコンペに追加しました。コンペタブで確認できます。`, 'info');
}

function sendAllToQueue() {
  const btns = document.querySelectorAll('#generate-result-area .btn-primary');
  btns.forEach(b => {
    b.disabled = true;
    b.textContent = '✅ 追加済み';
  });
  const qCount = document.getElementById('q-pending-count');
  if (qCount) qCount.textContent = parseInt(qCount.textContent) + btns.length;
  showToast(`全クリエイティブを入稿キューに追加しました。`, 'success');
}

/* ================================
   人間 vs AI コンペ
================================ */
function renderCompeteList() {
  const container = document.getElementById('compete-list');
  if (!container) return;
  container.innerHTML = COMPETE_PAIRS.map(pair => {
    const isRunning = pair.status === 'running';
    const winnerHuman = pair.winner === 'human';
    const winnerAI = pair.winner === 'ai';
    return `
    <div class="card" style="margin-bottom:24px;">
      <div class="card-header">
        <div class="card-title">
          ${isRunning ? '🟢 配信中:' : '✅ 完了:'} ${pair.theme}
        </div>
        <div style="display:flex;align-items:center;gap:10px;">
          <span class="media-badge ${MEDIA_META[pair.media]?.badge || ''}">${MEDIA_META[pair.media]?.emoji || ''} ${pair.media}</span>
          <span class="status-tag ${isRunning ? 'live' : 'approved'}">${isRunning ? '配信中' : '結果確定'}</span>
        </div>
      </div>
      <div class="card-body">
        <div class="compete-pair">
          <!-- 人間 -->
          <div class="compete-card human ${!isRunning && winnerHuman ? 'winner' : ''}">
            <div class="compete-header human">👤 人間制作 ${!isRunning && winnerHuman ? '🏆 勝利' : ''}</div>
            <div class="compete-thumb" style="background:${pair.human.bgGrad};">
              <span style="font-size:40px;">${pair.human.emoji}</span>
            </div>
            <div class="compete-body">
              <div class="compete-copy">${pair.human.copy}</div>
              ${renderScores(pair.human.scores, 'human', isRunning)}
            </div>
            ${!isRunning && winnerHuman ? '<div style="padding:10px 14px;background:#fff8e1;text-align:center;font-size:12px;font-weight:700;color:#f57f17;">このクリエイティブが次回生成のシードに昇格しました</div>' : ''}
          </div>

          <div class="vs-badge">VS</div>

          <!-- AI -->
          <div class="compete-card ai ${!isRunning && winnerAI ? 'winner' : ''}">
            <div class="compete-header ai">🤖 AI生成 ${!isRunning && winnerAI ? '🏆 勝利' : ''}</div>
            <div class="compete-thumb" style="background:${pair.ai.bgGrad};">
              <span style="font-size:40px;">${pair.ai.emoji}</span>
            </div>
            <div class="compete-body">
              <div class="compete-copy">${pair.ai.copy}</div>
              ${renderScores(pair.ai.scores, 'ai', isRunning)}
            </div>
            ${!isRunning && winnerAI ? '<div style="padding:10px 14px;background:#e0f2f1;text-align:center;font-size:12px;font-weight:700;color:#00695c;">このAI案が次回生成のシードに昇格しました</div>' : ''}
          </div>
        </div>
        ${isRunning ? '<div style="text-align:center;font-size:13px;color:var(--text-secondary);margin-top:8px;">配信中... 結果は自動集計されます</div>' : ''}
      </div>
    </div>`;
  }).join('');
}

function renderScores(scores, type, isRunning) {
  const pctCTR = Math.min(100, Math.round((scores.ctr / 5) * 100));
  const pctCVR = Math.min(100, Math.round((scores.cvr / 5) * 100));
  const pctCPA = Math.min(100, Math.round(((3000 - scores.cpa) / 2000) * 100));
  return `
  <div class="score-bar">
    <span class="score-label">CTR</span>
    <div class="score-fill-wrap"><div class="score-fill ${type}" style="width:${isRunning ? 0 : pctCTR}%;transition:width 1s ease;"></div></div>
    <span class="score-num">${isRunning ? '??%' : scores.ctr + '%'}</span>
  </div>
  <div class="score-bar">
    <span class="score-label">CVR</span>
    <div class="score-fill-wrap"><div class="score-fill ${type}" style="width:${isRunning ? 0 : pctCVR}%;transition:width 1.2s ease;"></div></div>
    <span class="score-num">${isRunning ? '??%' : scores.cvr + '%'}</span>
  </div>
  <div class="score-bar">
    <span class="score-label">CPA</span>
    <div class="score-fill-wrap"><div class="score-fill ${type}" style="width:${isRunning ? 0 : pctCPA}%;transition:width 1.4s ease;"></div></div>
    <span class="score-num">${isRunning ? '???' : '¥' + scores.cpa.toLocaleString()}</span>
  </div>`;
}

function openUploadHuman() {
  document.getElementById('upload-modal').style.display = 'flex';
}

function closeUploadModal() {
  document.getElementById('upload-modal').style.display = 'none';
}

function submitHumanCreative() {
  const name = document.getElementById('upload-name').value || '人間制作クリエイティブ';
  const copy = document.getElementById('upload-copy').value || 'コピーテキスト';
  const appeal = document.getElementById('upload-appeal').value;
  const media = document.getElementById('upload-media').value;

  const newPair = {
    id: COMPETE_PAIRS.length + 1,
    theme: `${media} — 追加コンペ`,
    media,
    status: 'running',
    human: {
      name, emoji: '👤',
      copy,
      scores: { ctr: 2.0, cvr: 2.0, cpa: 2000 },
      bgGrad: 'linear-gradient(135deg,#fff9c4,#fff176)',
    },
    ai: {
      name: `AI生成 (${appeal}訴求)`, emoji: '🤖',
      copy: GENERATED_TEMPLATES.find(t => t.hook === appeal.split('・')[0])?.copy || '最短翌日集荷。本がお金になります。',
      scores: { ctr: 3.0, cvr: 2.8, cpa: 1650 },
      bgGrad: 'linear-gradient(135deg,#e0f7fa,#b2ebf2)',
    },
    winner: null,
  };

  COMPETE_PAIRS.unshift(newPair);
  closeUploadModal();
  renderCompeteList();
  showToast(`「${name}」をコンペに追加しました！AIと対決開始です。`, 'success');
}

/* ================================
   入稿キュー
================================ */
function renderQueueList() {
  const container = document.getElementById('queue-list');
  if (!container) return;

  const statusLabel = { pending: '承認待ち', approved: '承認済み', submitted: '入稿済み', rejected: '差戻し', live: '配信中' };
  const statusTag = { pending: 'pending', approved: 'approved', submitted: 'submitted', rejected: 'rejected', live: 'live' };

  container.innerHTML = QUEUE_ITEMS.map(item => `
  <div class="queue-item" id="queue-${item.id}">
    <div class="queue-thumb">${item.emoji}</div>
    <div class="queue-info">
      <div class="queue-name">${item.name}</div>
      <div class="queue-detail">
        <span class="media-badge ${MEDIA_META[item.media]?.badge || ''}" style="padding:2px 8px;">${MEDIA_META[item.media]?.emoji || ''} ${item.media}</span>
        <span>サイズ: ${item.size}</span>
        <span>訴求: ${item.appeal}</span>
        <span>${item.generator} 制作</span>
        <span>作成: ${item.createdAt}</span>
        <span>予測CPA: ¥${item.cpaEst.toLocaleString()}</span>
      </div>
    </div>
    <div style="flex-shrink:0;">
      <span class="status-tag ${statusTag[item.status]}">${statusLabel[item.status]}</span>
    </div>
    <div class="queue-actions">
      ${item.status === 'pending' ? `
        <button class="btn btn-primary btn-sm" onclick="approveItem(${item.id})">✅ 承認</button>
        <button class="btn btn-danger btn-sm" onclick="rejectItem(${item.id})">❌ 差戻し</button>
      ` : ''}
      ${item.status === 'approved' ? `
        <button class="btn btn-accent btn-sm" onclick="submitItem(${item.id})">🚀 入稿</button>
        <button class="btn btn-danger btn-sm" onclick="rejectItem(${item.id})">❌ 差戻し</button>
      ` : ''}
      ${item.status === 'submitted' ? `<span style="font-size:12px;color:var(--text-secondary);">配信中</span>` : ''}
      ${item.status === 'rejected' ? `<button class="btn btn-outline btn-sm" onclick="approveItem(${item.id})">🔄 再承認</button>` : ''}
    </div>
  </div>
  `).join('');
}

function approveItem(id) {
  const item = QUEUE_ITEMS.find(i => i.id === id);
  if (!item) return;
  item.status = 'approved';
  renderQueueList();
  updateQueueCounts();
  showToast(`「${item.name}」を承認しました。`, 'success');
}

function rejectItem(id) {
  const item = QUEUE_ITEMS.find(i => i.id === id);
  if (!item) return;
  item.status = 'rejected';
  renderQueueList();
  updateQueueCounts();
  showToast(`「${item.name}」を差戻ししました。`, 'warning');
}

function submitItem(id) {
  const item = QUEUE_ITEMS.find(i => i.id === id);
  if (!item) return;
  item.status = 'submitted';
  renderQueueList();
  updateQueueCounts();
  showToast(`「${item.name}」を ${item.media} に自動入稿しました。`, 'success');
}

function approveAll() {
  QUEUE_ITEMS.filter(i => i.status === 'pending').forEach(i => { i.status = 'approved'; });
  renderQueueList();
  updateQueueCounts();
  showToast('全ての承認待ちクリエイティブを承認しました。', 'success');
}

function runAutoSubmit() {
  const approved = QUEUE_ITEMS.filter(i => i.status === 'approved');
  if (approved.length === 0) {
    showToast('承認済みのクリエイティブがありません。先に承認してください。', 'warning');
    return;
  }
  showToast(`${approved.length}件を自動入稿しています...`, 'info', 2000);
  setTimeout(() => {
    approved.forEach(i => { i.status = 'submitted'; });
    renderQueueList();
    updateQueueCounts();
    showToast(`${approved.length}件を各媒体に自動入稿しました！`, 'success');
  }, 2000);
}

function updateQueueCounts() {
  const el = id => document.getElementById(id);
  if (el('q-pending-count')) el('q-pending-count').textContent = QUEUE_ITEMS.filter(i => i.status === 'pending').length;
  if (el('q-approved-count')) el('q-approved-count').textContent = QUEUE_ITEMS.filter(i => i.status === 'approved').length;
  if (el('q-submitted-count')) el('q-submitted-count').textContent = QUEUE_ITEMS.filter(i => i.status === 'submitted').length;
  if (el('q-rejected-count')) el('q-rejected-count').textContent = QUEUE_ITEMS.filter(i => i.status === 'rejected').length;
}

/* ================================
   初期化
================================ */
document.addEventListener('DOMContentLoaded', () => {
  initDate();
  renderTrendChart();
  renderTopCreativesDashboard();
  renderBudgetSliders();
  renderPlanTable();
  filterCreatives();
  renderCompeteList();
  renderQueueList();
  updateQueueCounts();

  // スコアバーのアニメーションを遅延実行
  setTimeout(() => {
    document.querySelectorAll('.score-fill').forEach(el => {
      const target = el.style.width;
      el.style.width = '0';
      setTimeout(() => { el.style.width = target; }, 100);
    });
  }, 300);
});
