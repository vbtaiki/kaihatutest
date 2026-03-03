/**
 * バリューブックス ポイント経済圏
 * メインアプリケーション
 */

// ===========================
// 状態管理
// ===========================
let state = {
  balance: 2450,
  history: [
    { type: '買取ポイント獲得', detail: '5冊の買取（ポイント受取 +10%）', amount: +2200, date: '2026-02-07' },
    { type: 'ポイントで購入', detail: '「老子 道徳経」を購入', amount: -550, date: '2026-02-03' },
    { type: '買取ポイント獲得', detail: '3冊の買取（ポイント受取 +10%）', amount: +800, date: '2026-01-28' },
  ]
};

// ===========================
// 初期化
// ===========================
document.addEventListener('DOMContentLoaded', () => {
  renderHistory();
  updateBalanceDisplay();

  // 買取金額の入力に連動して表示を更新
  const amountInput = document.getElementById('buyback-amount');
  if (amountInput) {
    amountInput.addEventListener('input', updateBuybackOptions);
  }
});

// ===========================
// 残高表示の更新
// ===========================
function updateBalanceDisplay() {
  document.getElementById('balance').textContent = state.balance.toLocaleString();
  document.getElementById('point-display').textContent = state.balance.toLocaleString();
}

// ===========================
// 取引履歴の描画
// ===========================
function renderHistory() {
  const list = document.getElementById('history-list');
  list.innerHTML = state.history.map(item => `
    <div class="history-item">
      <div class="history-left">
        <div class="history-type">${item.type}</div>
        <div class="history-detail">${item.detail}</div>
        <div class="history-date">${item.date}</div>
      </div>
      <div class="history-amount ${item.amount >= 0 ? 'plus' : 'minus'}">
        ${item.amount >= 0 ? '+' : ''}${item.amount.toLocaleString()} pt
      </div>
    </div>
  `).join('');
}

// ===========================
// 買取モーダル
// ===========================
function openBuyback() {
  document.getElementById('buyback-modal').classList.add('active');
  updateBuybackOptions();
}

function updateBuybackOptions() {
  const amount = parseInt(document.getElementById('buyback-amount').value) || 0;
  const bonus = Math.floor(amount * 1.1);
  document.getElementById('cash-amount').textContent = `¥${amount.toLocaleString()}`;
  document.getElementById('point-amount').textContent = `${bonus.toLocaleString()} pt`;
}

function selectOption(type) {
  document.getElementById('opt-cash').classList.toggle('selected', type === 'cash');
  document.getElementById('opt-point').classList.toggle('selected', type === 'point');
}

function submitBuyback() {
  const amount = parseInt(document.getElementById('buyback-amount').value) || 0;
  const isPoint = document.getElementById('opt-point').classList.contains('selected');
  const received = isPoint ? Math.floor(amount * 1.1) : amount;

  if (isPoint) {
    state.balance += received;
    state.history.unshift({
      type: '買取ポイント獲得',
      detail: `買取金額 ¥${amount.toLocaleString()}（ポイント受取 +10%）`,
      amount: +received,
      date: new Date().toISOString().split('T')[0]
    });
    updateBalanceDisplay();
    renderHistory();
    showToast(`🎉 ${received.toLocaleString()} pt を獲得しました！`);
  } else {
    showToast(`💴 ¥${amount.toLocaleString()} を銀行口座に振り込みます`);
  }

  closeModal('buyback-modal');
}

// ===========================
// 購入モーダル
// ===========================
function openShop() {
  document.getElementById('shop-modal').classList.add('active');
}

function buyBook(price, title) {
  if (state.balance < price) {
    showToast('⚠️ ポイントが足りません');
    return;
  }

  state.balance -= price;
  state.history.unshift({
    type: 'ポイントで購入',
    detail: `「${title}」を購入`,
    amount: -price,
    date: new Date().toISOString().split('T')[0]
  });

  updateBalanceDisplay();
  renderHistory();
  closeModal('shop-modal');
  showToast(`📚 「${title}」を購入しました！`);
}

// ===========================
// モーダル共通
// ===========================
function closeModal(id) {
  document.getElementById(id).classList.remove('active');
}

// モーダル外クリックで閉じる
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal')) {
    e.target.classList.remove('active');
  }
});

// ===========================
// トースト通知
// ===========================
function showToast(message) {
  // 既存のトーストを削除
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  document.body.appendChild(toast);

  requestAnimationFrame(() => {
    toast.classList.add('show');
  });

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
