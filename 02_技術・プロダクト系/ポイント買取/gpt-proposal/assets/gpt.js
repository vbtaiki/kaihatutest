(() => {
  const page = document.body?.dataset?.gptPage || "unknown";

  const PAGE_SUGGESTIONS = {
    mypage: ["今日のおすすめを3つ", "今週の読書プランを作る", "ポイントの使い方を最適化"],
    offer: ["最適な受取方法を提案して", "ボーナスの意味を短く", "損しない設定にして"],
    recommendations: ["理由を3行で", "今の気分に合わせて絞り込み", "ポイント内で買える順に"],
    "rank-system": ["最短で次ランクに行く方法", "今月のミッションを作る", "特典を一言で"],
    "apply-complete": ["次にやるべきことは？", "ポイントを賢く使う案", "今すぐ買うならどれ？"],
    unknown: ["どこから始める？", "今の状態を要約して", "次の一手を提案して"],
  };

  const reply = (text) => {
    // A lightweight, deterministic "GPT-like" responder (no network).
    const t = (text || "").toLowerCase();
    const base = {
      head: "了解。いまの目的と制約を3点で整理して、最短手順を提案します。\n",
      bullets: (items) => items.map((x) => `- ${x}`).join("\n"),
    };

    if (page === "recommendations") {
      if (t.includes("理由") || t.includes("3") || t.includes("三")) {
        return (
          base.head +
          base.bullets([
            "あなたの直近の買取傾向（技術/環境/ビジネス）と近いテーマを優先",
            "難易度が急に上がらないよう“次の一段”を混ぜる",
            "ポイント内で買える確率が高い価格帯から提示",
          ]) +
          "\n\nmini: 右下のチップから「今の気分」を選ぶと、提案が変わります。"
        );
      }
      if (t.includes("絞") || t.includes("気分")) {
        return (
          base.head +
          base.bullets([
            "5分で読める軽め → 入門/エッセイ寄り",
            "ガッツリ学びたい → 専門/体系書",
            "仕事に効く → 実務/ケーススタディ",
          ]) +
          "\n\nmini: どれでいきます？（軽め / ガッツリ / 仕事）"
        );
      }
      return (
        base.head +
        base.bullets([
          "まず“何を得たいか”（学び/癒し/実務）を決める",
          "次に“読了できる分量”を決める（薄め/普通/厚め）",
          "その条件で3冊に絞る",
        ])
      );
    }

    if (page === "offer") {
      if (t.includes("受取") || t.includes("最適") || t.includes("損")) {
        return (
          base.head +
          base.bullets([
            "本を買う予定がある → ポイント受取を維持（取り回し最強）",
            "早く確定したい → ソクフリON（待ち時間コスト削減）",
            "迷う → “ポイントON + ソクフリON”が期待値最大（このデモ設定）",
          ]) +
          "\n\nmini: 何を優先します？（お得 / 早い / シンプル）"
        );
      }
      if (t.includes("ボーナス")) {
        return (
          "ボーナスは“行動を早く・確実に”してくれる代わりに上乗せされる設計です。\n- ソクフリ: 査定後の確定を速くする\n- ポイント: 次の購入に繋がる（上乗せ大きめ）"
        );
      }
      return (
        base.head +
        base.bullets([
          "優先順位（お得/早さ/安心）を選ぶ",
          "ON/OFFの意味を1行で確認",
          "確定後の次アクション（おすすめ/ランク）に繋げる",
        ])
      );
    }

    if (page === "mypage") {
      if (t.includes("プラン") || t.includes("今週")) {
        return (
          base.head +
          base.bullets([
            "今週のテーマ：①仕事 ②趣味 ③視野を広げる（各1冊）",
            "読書時間：平日10分×3 + 週末30分×1（無理しない）",
            "次の一手：今日の1冊を決めて“買う or 売る”に分岐",
          ]) +
          "\n\nmini: 週の読書時間はどれくらいですか？（10分/30分/60分）"
        );
      }
      if (t.includes("おすすめ") || t.includes("3")) {
        return (
          base.head +
          base.bullets([
            "学び：データで見る未来の日本（視野が広がる）",
            "実務：UXデザインの真髄（すぐ効く）",
            "深掘り：ディープラーニング 2026（次の段）",
          ]) +
          "\n\nmini: どれを“今日の1冊”にします？"
        );
      }
      return (
        base.head +
        base.bullets([
          "いまの状態を要約（ポイント/買取/購入/ランク）",
          "次の一手を1つに絞る",
          "迷いがある場合は3問で診断して決める",
        ])
      );
    }

    if (page === "rank-system") {
      if (t.includes("最短") || t.includes("ミッション") || t.includes("次")) {
        return (
          base.head +
          base.bullets([
            "まず“今月の達成条件”を1つ決める（例：＋20冊）",
            "次に“週の行動”に分解（例：週5冊の整理）",
            "最後に“買い物”はポイント内の小額から（継続優先）",
          ]) +
          "\n\nmini: 今月の目標は？（ゴールド/ポイント/本棚整理）"
        );
      }
      return (
        base.head +
        base.bullets([
          "ランク＝継続利用の見える化（次が分かる）",
          "特典＝今やる理由（小さな得）",
          "ミッション＝行動を迷わない仕組み",
        ])
      );
    }

    if (page === "apply-complete") {
      return (
        base.head +
        base.bullets([
          "今すぐ買う：ポイント内で1冊だけ（成功体験を作る）",
          "迷う：おすすめで3冊→1冊に絞る（理由つき）",
          "育てる：ランクで“今月のミッション”を設定",
        ])
      );
    }

    return (
      base.head +
      base.bullets([
        "いまのページで達成したいことを1つ選ぶ",
        "制約（時間/お金/迷い）を1つ選ぶ",
        "その条件で次の一手を提示する",
      ])
    );
  };

  function createUI() {
    const fab = document.createElement("div");
    fab.className = "gpt-fab";
    fab.setAttribute("role", "button");
    fab.setAttribute("aria-label", "GPTに相談");
    fab.innerHTML = `<span class="gpt-fab-dot"></span><small>GPTに相談</small>`;

    const panel = document.createElement("div");
    panel.className = "gpt-panel";
    panel.innerHTML = `
      <header>
        <div class="title">
          <strong>GPTコンシェルジュ</strong>
          <span>このデモ内で“次の一手”を一緒に決めます</span>
        </div>
        <div class="actions">
          <button class="gpt-icon-btn" data-gpt-clear type="button">↺</button>
          <button class="gpt-icon-btn" data-gpt-close type="button">✕</button>
        </div>
      </header>
      <div class="gpt-body" data-gpt-body></div>
      <div class="gpt-footer">
        <input class="gpt-input" data-gpt-input placeholder="例）理由を3行で / 最適な設定は？" />
        <button class="gpt-send" data-gpt-send type="button">送信</button>
      </div>
    `;

    document.body.appendChild(fab);
    document.body.appendChild(panel);

    const bodyEl = panel.querySelector("[data-gpt-body]");
    const inputEl = panel.querySelector("[data-gpt-input]");
    const sendBtn = panel.querySelector("[data-gpt-send]");

    function pushMsg(kind, text) {
      const row = document.createElement("div");
      row.className = `gpt-msg ${kind}`;
      const bubble = document.createElement("div");
      bubble.className = "bubble";
      if (kind === "assistant" && text.includes("\n\nmini:")) {
        const [main, mini] = text.split("\n\nmini:");
        bubble.innerHTML = `<strong>${escapeHtml(main.split("\n")[0])}</strong>\n${escapeHtml(main.split("\n").slice(1).join("\n")).replace(/\n/g,"<br/>")}<span class="mini">${escapeHtml(mini.trim())}</span>`;
      } else {
        bubble.textContent = text;
      }
      row.appendChild(bubble);
      bodyEl.appendChild(row);
      bodyEl.scrollTop = bodyEl.scrollHeight;
    }

    function renderSuggestions() {
      const wrap = document.createElement("div");
      wrap.className = "gpt-suggestions";
      (PAGE_SUGGESTIONS[page] || PAGE_SUGGESTIONS.unknown).forEach((label) => {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "gpt-chip";
        b.textContent = label;
        b.addEventListener("click", () => {
          inputEl.value = label;
          doSend();
        });
        wrap.appendChild(b);
      });
      bodyEl.appendChild(wrap);
      bodyEl.scrollTop = bodyEl.scrollHeight;
    }

    function doSend() {
      const text = (inputEl.value || "").trim();
      if (!text) return;
      inputEl.value = "";
      pushMsg("user", text);
      const ans = reply(text);
      pushMsg("assistant", ans);
      renderSuggestions();
    }

    fab.addEventListener("click", () => {
      panel.classList.toggle("is-open");
      if (panel.classList.contains("is-open") && !panel.dataset.booted) {
        panel.dataset.booted = "1";
        pushMsg("assistant", reply("はじめる"));
        renderSuggestions();
      }
      setTimeout(() => inputEl.focus(), 0);
    });

    panel.querySelector("[data-gpt-close]").addEventListener("click", () => {
      panel.classList.remove("is-open");
    });

    panel.querySelector("[data-gpt-clear]").addEventListener("click", () => {
      bodyEl.innerHTML = "";
      pushMsg("assistant", reply("はじめる"));
      renderSuggestions();
    });

    sendBtn.addEventListener("click", doSend);
    inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter") doSend();
    });

    // Allow in-page buttons to trigger the concierge
    window.__gptConcierge = {
      openWith(text) {
        panel.classList.add("is-open");
        if (!panel.dataset.booted) {
          panel.dataset.booted = "1";
          pushMsg("assistant", reply("はじめる"));
          renderSuggestions();
        }
        inputEl.value = text || "";
        if (text) doSend();
      },
    };
  }

  function escapeHtml(str) {
    return String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  document.addEventListener("DOMContentLoaded", () => {
    createUI();

    // Bind optional buttons
    document.querySelectorAll("[data-gpt-ask]").forEach((el) => {
      el.addEventListener("click", () => {
        const q = el.getAttribute("data-gpt-ask") || "次の一手は？";
        window.__gptConcierge?.openWith(q);
      });
    });
  });
})();

