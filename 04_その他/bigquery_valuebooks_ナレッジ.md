# ValueBooks BigQuery ナレッジ

## 接続情報
- **GCPプロジェクト**: `valuebooks-ga4`
- **Chromeプロファイル**: 仕事用（`switch_browser`で「仕事用」に接続）
- **リージョン**: asia-northeast1
- **注意**: INFORMATION_SCHEMA へのアクセス権限なし。テーブル構造確認は `SELECT * ... LIMIT` で行う

## 販売区分（hanbai_kbn）マスター
| コード | 販路名 |
|---|---|
| A1 | Amazon |
| R1 | 楽天 (Rakuten) |
| V1 | ValueBooks直販 |
| C1 | メルカリ (Mercari) |
| M1 | ラクマ (Rakuma) |
| Y1 | Yahoo |

## サイトコード（site_code）マスター
| コード | サイト名 |
|---|---|
| MA1 | ValueBooks（メイン） |
| CH1 | Charibon |
| VA1 | Vaboo |

## 主要データセット一覧

### valuebooks_master（★売上分析向け）
| テーブル名 | 説明 | 主要カラム |
|---|---|---|
| `hassou_master` | 発送マスター（売上分析のメインテーブル） | ship_date(STRING), order_id, hanbai_kbn, hassou_step_code, hassou_num, pack_num, vbsku, condition, title, item_price, shipping_price, nebiki, genpin_id, location |
| `hassou_item_master` | 発送アイテムマスター（取込日付あり） | torikomi_date(STRING), order_id, step_kbn, hanbai_kbn, hassou_step_code, hassou_num, vbsku, condition, title, item_price, shipping_price, nebiki, genpin_id |
| `satei_head_master` | 査定ヘッダーマスター | 未調査 |
| `shitadori_used_mas` | 下取中古マスター | 未調査 |
| `shuppin_total` | 出品合計 | 未調査 |

### for_bi（買取広告・トラフィック分析向け ※一部停止）
| テーブル名 | 説明 | データ期間 | 主要カラム |
|---|---|---|---|
| `kaitori_master_ad` | 買取Web広告マスター | 2024-01〜2026-02（更新中） | moushikomi_ym(STRING), moushikomi_date(STRING), category, moushikomi_cnt, coupon_web_cnt, coupon_other_cnt, ad_cnt, ad_cost |
| `all_traffic_report` | 全トラフィックレポート（チラシ含む） | 2017-01〜**2025-03-07で停止⚠️** | site_code, moushikomi_ym(STRING 'YYYY/MM/DD HH:MM:SS'), all_category_01, cs_type(新規/既存), class(A/B/C/N), cnt, cnt_ym_total, cnt_ym_total_abc, coupon_category_num, table_name, ratio_ym_total, ratio_ym_total_abc |

> ⚠️ **`all_traffic_report` は2025/03/07で停止**。代替として `external_source.kaitori_master_bi` を使用する（下記参照）

#### kaitori_master_ad のcategory一覧
| category | 媒体 | タイプ | 備考 |
|---|---|---|---|
| web_google_new | Google | 新規 | 最大の広告チャネル |
| web_google_rt | Google | RT | 2025-11以降データなし |
| web_meta_new | Meta(Facebook/Instagram) | 新規 | 急成長中 |
| web_meta_rt | Meta | RT | CPA異常高 |
| web_criteo_new | Criteo | 新規 | CPA悪化中 |
| web_criteo_rt | Criteo | RT | |
| web_yahoo_new | Yahoo | 新規 | |
| web_yahoo_rt | Yahoo | RT | |
| web_x_new | X(Twitter) | 新規 | ad_cost未連携の月が多い |
| web_SMN_new | SMN | 新規 | 小規模 |
| web_line_new | LINE | 新規 | 小規模 |
| web_jimoty_new | ジモティー | 新規 | 1ヶ月のみ |

#### all_traffic_report のall_category_01一覧
| category | 説明 |
|---|---|
| `fl_rakuten` | 楽天チラシ同梱（月5,000〜7,000件、新規63%） |
| `fl_other` | その他チラシ同梱（オイシックス等、月700〜2,200件、新規71%） |
| `fl_vb` | VBチラシ（月3,700〜4,800件、既存58%） |
| `mm_rakuten` | 楽天メルマガ |
| `colabo` | コラボ |
| `charibon` | チャリボン |
| `cs` | カスタマーサービス |
| `organic` | オーガニック検索 |
| `referral` | リファラル |
| `social` | ソーシャル |
| `blog` | ブログ |
| `web_ad_*` | 各種Web広告（google_display, facebook_display等） |
| `web_site_*` | Webサイト経由 |

### valuebooks_db（★生データ・リアルタイム）
| テーブル名 | 説明 | データ鮮度 | 主要カラム |
|---|---|---|---|
| `hassou_head` | 発送ヘッダー | リアルタイム | hassou_num, purchase_date(TIMESTAMP), zip_code1(mask), ship_state, hassou_price_item, hassou_total_price, youchuui_code, rbo_number |
| `hassou_hikiate` | 発送引当（明細） | リアルタイム | hassou_num, meisai_renban, pack_num, seller_sku, catalog_id, genpin_barcode, vbsku, condition_code_vb, title, item_price, shipping_price, tehai_status, souko_code各種, hikiate_status, genpin_id, location |
| `kaitori` | 買取トランザクション | **リアルタイム（本日まで）** | kaitori_num, customer_id, site_code(MA1/CH1/VA1), torihiki_jyotai, torihiki_status_code, customer_status_code, moushikomi_dtm(TIMESTAMP), hurikomi_houhou, torihiki_kekka, torihiki_kekka_dtm, torihiki_end_dtm, campaign_code, dantai_code, kigyou_code, souryou_mode |
| `kaitori_campaign` | 買取キャンペーン紐付け | リアルタイム | id, kaitori_num, campaign_code, introducer_id, ins_dtm |
| `kaitori_hurikomi` | 買取振込 | 未詳細調査 | |
| `kaitori_master` | 買取マスター | 未詳細調査 | |
| `customer*` | 顧客関連テーブル群 | 未詳細調査 | |
| `m_shoshi*` | 書誌マスター群 | 未詳細調査 | |
| `m_genpin` | 現品マスター | 未詳細調査 | |

#### campaign_code の命名規則（推定）
| プレフィックス | 意味 | 例 |
|---|---|---|
| ALL2025xxA | 全員向け月次キャンペーン | ALL202601A (月16,000〜20,000件) |
| SOKU* | 即買取 | SOKU1 (最多) |
| SOKULINE* | LINE即買取 | SOKULINE2 |
| MAIL* | メール経由 | MAIL2, MAIL1CH |
| SLIST* | スマートリスト（倉庫/店舗別？） | SLISTCOEDO26, SLISTONIBUS26 |
| LT* | リーフレット/チラシ？ | LT251XHT, LT251XHS |
| FB* | Facebook | FB2511NW |
| CS* | Criteo? | CS23RTA |
| *FL | フライヤー（チラシ）関連 | R2311FL, LT246FL |
| ALLCHARIBON* | Charibon向け | ALLCHARIBONSOURYOU0 |

### external_source（★★★ 最重要：マーケティング・買取分析の中心）

> **`all_traffic_report`（2025/03停止）の代替データがここにある！**
> 毎日自動更新されており、チラシ・広告・オーガニック等すべてのチャネルデータが揃っている。

#### kaitori_master_bi（★★★ `all_traffic_report`の実質的な後継）
| 項目 | 内容 |
|---|---|
| テーブル名 | `external_source.kaitori_master_bi` |
| 行数 | 約152万行 |
| 期間 | 2017-07 〜 **本日まで（毎日更新）** |
| 説明 | 買取申込1件1行のBI用マスター。チャネル帰属・広告費・GA4流入元・顧客属性をすべて結合済み |

**主要カラム（抜粋）:**
| カラム | 型 | 説明 |
|---|---|---|
| `kaitori_num` | STRING | 買取番号 |
| `customer_id` | STRING | 顧客ID |
| `moushikomi_dtm` | DATE | 申込日 |
| `moushikomi_ym` | STRING | 申込年月 |
| `site_code` | STRING | MA1/CH1/VA1 |
| `cs_type` | STRING | new/repeat |
| `all_category` | STRING | **チャネル分類（旧all_traffic_reportと同じ体系）** |
| `coupon_code` | STRING | 利用クーポンコード |
| `coupon_media` | STRING | クーポン媒体（CS/楽天/オイシックス等） |
| `ad_use` | STRING | 広告利用区分（web_ad/flyer/other） |
| `ga_sourceMedium` | STRING | GA4流入元 |
| `ga_landingPagePath` | STRING | ランディングページ |
| `ga_campaign` | STRING | GA4キャンペーン |
| `total_cnt` | INT | 査定冊数 |
| `ok_cnt` | INT | 買取OK冊数 |
| `total` | INT | 買取金額 |
| `flyer_cost` | INT | チラシコスト |
| `total_cost` | FLOAT | 総コスト |
| `class` | STRING | A/B/C/N |
| `generation` | STRING | 年代（30代/40代等） |
| `gender` | STRING | 性別 |
| `state` | STRING | 都道府県 |

**all_category の一覧（2025年9月〜の件数順）:**
| category | 説明 | 月間件数目安 |
|---|---|---|
| `cs` | カスタマーサービス経由 | 約5,000件 |
| `fl_rakuten` | 楽天チラシ同梱 | 約4,500件 |
| `fl_vb` | VBチラシ | 約3,800件 |
| `fl_other` | その他チラシ（オイシックス等） | 約2,000件 |
| `charibon` | チャリボン | 約1,200件 |
| `etc` | その他 | 約1,100件 |
| `organic` | オーガニック検索 | 約1,000件 |
| `web_site_cs` | Webサイト（CS経由） | 約850件 |
| `web_ad_normal` | Web広告（通常） | 約650件 |
| `colabo` | コラボ | 約400件 |
| `mm_rakuten` | 楽天メルマガ | 約370件 |
| `web_ad_facebook_display_new` | Facebook広告（新規） | 約280件 |
| `web_ad_display` | ディスプレイ広告 | 約200件 |
| `web_ad_facebook_display` | Facebook広告 | 約200件 |
| `mm_other` | その他メルマガ | 約150件 |
| `social` | ソーシャル | 約95件 |
| `web_ad_criteo_display_new` | Criteo広告（新規） | 約75件 |
| `web_ad_x_display_new` | X広告（新規） | 小規模 |
| `blog` | ブログ | 小規模 |

#### web_ad_month_report（★★ Web広告の月次レポート）
| 項目 | 内容 |
|---|---|
| テーブル名 | `external_source.web_ad_month_report` |
| 行数 | 907行 |
| 期間 | 2021-01 〜 2026-01（毎月更新） |
| 説明 | Web広告の月次実績。impression/click/conversion/CPA を媒体×新規・RT別に集計 |

**主要カラム:** event_date(DATE), site_name, media, category(新規/リターゲティング/指名/一般検索), impression, click_cnt, click_ratio, click_cost, conversion_cnt, conversion_coupon_cnt, cpa, all_cost, conversion_rate

**media一覧:** Google, Googleデマンド, Google P-MAX, FB/IG, FB/IG 誕生日, Criteo, Yahoo, LINE, X, Microsoft, SmartNews, ジモティー

> `for_bi.kaitori_master_ad` より詳細（imp/click/CVR付き）。Web広告分析はこちらを推奨。

#### moushikomi_shuka（★★ 申込・出荷の日次データ）
| 項目 | 内容 |
|---|---|
| テーブル名 | `external_source.moushikomi_shuka` |
| 行数 | 約56万行 |
| 期間 | 2023-01 〜 **本日まで（毎日更新）** |
| 説明 | 買取申込・出荷を日次×サイト×フォームタイプ×新規既存で集計 |

**主要カラム:** moushikomi_date(DATE), site_code, form_type(normal/lp/thanks/other), cs_type(new/repeat), state(都道府県), cnt, box_cnt, total_cnt, ok_cnt

#### その他のexternal_sourceテーブル（全70テーブル）
| テーブル名 | 説明 | 行数 | 更新 |
|---|---|---|---|
| `kaitori_campaign_all` | 全キャンペーン一覧 | 16,541 | 毎日 |
| `kaitori_tokuten_customer` | 買取特典顧客 | 377,324 | 毎日 |
| `kaitori_tokuten_duplication_customer` | 買取特典重複顧客 | 1,012,564 | 毎日 |
| `coupon_code_count_report` | クーポン利用レポート | 241,936 | 毎日 |
| `coupon_code_count_report_search` | クーポン検索レポート | 4,490 | 毎日 |
| `coupon_code_quolity_report` | クーポン品質レポート | 450,422 | 毎日 |
| `flyer_master_all` | チラシマスター（全種） | 1,201 | 毎日 |
| `flyer_master_all_and_simulation` | チラシ＋シミュレーション | 28,811 | 毎日 |
| `flyer_master_rakuten` | 楽天チラシマスター | 651 | 毎日 |
| `flyer_master_other` | その他チラシマスター | 445 | 毎日 |
| `flyer_master_vb` | VBチラシマスター | 357 | 毎日 |
| `flyer_master_oisix` | オイシックスチラシ | 215 | 毎日 |
| `flyer_copies_calendar` | チラシ配布カレンダー | 15,122 | 毎日 |
| `flyer_simulation` | チラシシミュレーション | 411 | 毎日 |
| `kaitori_simulation_report` | 買取シミュレーション | 4,370 | 毎日 |
| `hassou_count` | 発送件数 | 1,153 | 毎日 |
| `order_vb_report` | VB注文レポート | 43,269 | 毎日 |
| `order_vb_cs_report` | VB注文CS別レポート | 463,765 | 毎日 |
| `order_vb_customer_result` | 顧客別注文結果 | 61,751,114 | 毎日 |
| `ga4_vb_latest` | GA4 VB最新データ | 604,612 | 毎日 |
| `ga4_va_latest` | GA4 Vaboo最新データ | 6,026 | 毎日 |
| `ua_master` | UA（旧GA）マスター | 858,351 | 毎日 |
| `kaitori_form_type` | 買取フォーム種別（GA4連携） | 665,587 | 毎日 |
| `web_ad_master` | Web広告マスター | 10,304 | 月次 |
| `web_ad_facebook` | Facebook広告明細 | 5,998 | 月次 |
| `web_ad_google-yahoo` | Google/Yahoo広告明細 | 810 | 月次 |
| `affliate_rentracks_all` | アフィリエイト（レントラックス） | 69,227 | 停止 |
| `affliate_a8_all` | アフィリエイト（A8） | 21,806 | 停止 |

### ga_source（★ GAセッション・CV分析）
| テーブル名 | 説明 | 行数 | 更新 |
|---|---|---|---|
| `ga_session_comp_table` | GAセッション比較テーブル | 30,399,182 | 毎日 |
| `ga_landing_comp` | ランディングページ比較 | 4,873,080 | 毎日 |
| `ga_cv_transaction` | CVトランザクション | 2,409,879 | 毎日 |
| `ga_purchase_comp_table` | 購入比較テーブル | 491,384 | 毎日 |
| `ga_page_transition` | ページ遷移 | 11,355,706 | 毎日 |
| `search_keyword_extract` | 検索キーワード | 18,045,425 | 毎日 |

### from_marketingcloud（マーケティングクラウド連携）
| テーブル名 | 説明 | 行数 | 更新 |
|---|---|---|---|
| `kaitori_conversion_answers_union` | 買取コンバージョンアンケート | 128,820 | 毎日 |

### その他データセット
| データセット | 用途 |
|---|---|
| `ad_google_*` | Google広告（charibon, nomad, vaboo, valuebooks） |
| `analytics_*` | GA4データ（4つ） |
| `ecosystem` | エコシステム（2025-04停止） |
| `searchconsole_*` | Search Console（charibon, vaboo, valuebooks） |
| `valuebooks_collabo` | コラボ（32テーブル、一部毎日更新） |
| `valuebooks_ichikawa` | 市川（hikiate_count, shitadori_look等） |
| `valuebooks_meta` | メタデータ |
| `valuebooks_ml` / `_ml_us` | 機械学習 |
| `valuebooks_preservation` | 保存 |
| `valuebooks_summary` | サマリー（satei_summary、2024-05停止） |
| `valuebooks_taihi` | 退避 |
| `valuebooks_views` | ビュー |
| `valuebooks_youtube` | YouTube |
| `vb_production_from_s3` | S3からの本番データ（120テーブル、毎日更新） |
| `vb_production_marketing_dataset` | 本番マーケティング |
| `vbproduction4marketing` | マーケティング用本番データ |

## よく使うクエリ

### 販路別 月次売上・単価
```sql
SELECT
  SUBSTR(ship_date, 1, 7) as month,
  CASE hanbai_kbn
    WHEN 'A1' THEN 'Amazon'  WHEN 'R1' THEN 'Rakuten'
    WHEN 'V1' THEN 'VB直販'  WHEN 'C1' THEN 'メルカリ'
    WHEN 'M1' THEN 'ラクマ'  WHEN 'Y1' THEN 'Yahoo'
    ELSE hanbai_kbn
  END as channel,
  COUNT(*) as items_sold,
  SUM(item_price) as total_sales,
  ROUND(AVG(item_price), 0) as avg_unit_price
FROM `valuebooks-ga4.valuebooks_master.hassou_master`
WHERE ship_date >= '2025-09-01' AND ship_date < '2026-03-01'
GROUP BY month, channel
ORDER BY month, total_sales DESC
```

### 買取Web広告 月次CPA分析
```sql
SELECT moushikomi_ym, category, moushikomi_cnt, ad_cnt, ad_cost,
  CASE WHEN moushikomi_cnt > 0 THEN ROUND(ad_cost / moushikomi_cnt, 0) ELSE NULL END as cpa
FROM `valuebooks-ga4.for_bi.kaitori_master_ad`
WHERE moushikomi_date >= '2025-09-01'
ORDER BY moushikomi_ym, ad_cost DESC
```

### チラシ同梱 月次申込数（新規/既存別）— ★新しいクエリ（kaitori_master_bi版）
```sql
SELECT
  moushikomi_ym as ym,
  all_category,
  cs_type,
  COUNT(*) as total_cnt
FROM `valuebooks-ga4.external_source.kaitori_master_bi`
WHERE all_category LIKE 'fl_%' AND moushikomi_dtm >= '2024-04-01'
GROUP BY ym, all_category, cs_type
ORDER BY ym, all_category, cs_type
```

### チラシ同梱 月次申込数（旧クエリ ※2025/03以前のみ）
```sql
SELECT SUBSTR(moushikomi_ym, 1, 7) as ym, all_category_01, cs_type,
  SUM(CAST(cnt AS INT64)) as total_cnt
FROM `valuebooks-ga4.for_bi.all_traffic_report`
WHERE all_category_01 LIKE 'fl_%' AND moushikomi_ym >= '2024/04' AND table_name = '合計'
GROUP BY ym, all_category_01, cs_type
ORDER BY ym, all_category_01, cs_type
```

### 全チャネル別 月次買取申込数（★推奨クエリ）
```sql
SELECT
  moushikomi_ym,
  all_category,
  cs_type,
  COUNT(*) as kaitori_cnt,
  SUM(total_cnt) as total_items,
  SUM(total) as total_amount,
  ROUND(AVG(total), 0) as avg_amount
FROM `valuebooks-ga4.external_source.kaitori_master_bi`
WHERE moushikomi_dtm >= '2025-04-01'
GROUP BY moushikomi_ym, all_category, cs_type
ORDER BY moushikomi_ym, kaitori_cnt DESC
```

### Web広告 月次パフォーマンス（impression/click/CVR付き）
```sql
SELECT
  event_date, media, category,
  impression, click_cnt, click_ratio,
  conversion_cnt, conversion_rate,
  all_cost, cpa
FROM `valuebooks-ga4.external_source.web_ad_month_report`
WHERE event_date >= '2025-01-01'
ORDER BY event_date DESC, all_cost DESC
```

### 買取申込 直近キャンペーン別件数
```sql
SELECT c.campaign_code, COUNT(DISTINCT c.kaitori_num) as kaitori_cnt
FROM `valuebooks-ga4.valuebooks_db.kaitori_campaign` c
JOIN `valuebooks-ga4.valuebooks_db.kaitori` k ON c.kaitori_num = k.kaitori_num
WHERE k.moushikomi_dtm >= '2025-09-01'
GROUP BY c.campaign_code
ORDER BY kaitori_cnt DESC LIMIT 30
```

## データ型の注意
- `ship_date` は **STRING型**（'YYYY-MM-DD'形式）。FORMAT_DATE()は使えない。SUBSTR()で月を抽出する
- `torikomi_date` も STRING型
- `moushikomi_ym`（all_traffic_report）は **STRING型**（'YYYY/MM/DD HH:MM:SS'形式）。SUBSTR()で年月抽出
- `moushikomi_date`（kaitori_master_ad）は **STRING型**（'YYYY-MM-DD'形式）
- `moushikomi_dtm`（kaitori）は **TIMESTAMP型**
- `purchase_date`（hassou_head）は TIMESTAMP型
- 個人情報カラム（zip_code, address等）は「mask」「マスク」でマスキングされている
- BigQueryの予約語 `rows` はエイリアスに使えない → `row_cnt` 等にする

## データパイプラインの状況

### 解決済み
- ~~`all_traffic_report`が2025/03で停止~~
  → **`external_source.kaitori_master_bi`で代替可能**（2017-07〜本日まで、毎日更新）
  → 同じ`all_category`体系で、さらにGA4流入元・広告費・顧客属性も結合済み
  → チラシ同梱（fl_rakuten/fl_vb/fl_other）のデータも最新まで取得可能

### 残存課題
- `for_bi.kaitori_master_ad` の行数が0（テーブル定義のみ？）。実データは `external_source.web_ad_month_report` で取得可能
- `ecosystem` データセットが2025-04で停止
- `valuebooks_summary.satei_summary` が2024-05で停止

## 未調査・追加調査が必要なテーブル
- `valuebooks_master.shuppin_total` - 出品合計データ
- `valuebooks_master.satei_head_master` - 査定データ（買取分析）
- `valuebooks_db.kaitori_hurikomi` - 買取振込（金額分析）
- `valuebooks_db.kaitori_master` - 買取マスター
- `valuebooks_db.m_shoshi*` テーブル群 - 書誌（商品）マスター
- `valuebooks_db.m_genpin` - 現品マスター（在庫分析）
- `vb_production_from_s3` - S3本番データ（120テーブル、customer/hassou/shelfなど）
- `external_source.order_vb_customer_result` - 顧客別注文結果（6,175万行、巨大）

## 更新履歴
- 2026-02-27: 分析データセットの仕分けを実施。28データセットをS/A/B/C/D判定。詳細は10_分析データセット仕分けシート.md
- 2026-02-27: `external_source` データセットを詳細調査。`kaitori_master_bi`が`all_traffic_report`の代替として使えることを発見。`web_ad_month_report`、`moushikomi_shuka`、`ga_source`の情報を追加。
## 分析データセット仕分け（2026-02-27実施）

> 詳細は [10_分析データセット仕分けシート.md](../02_技術・プロダクト系/AIファースト開発移行/10_分析データセット仕分けシート.md) を参照

| 判定 | データセット |
|------|------------|
| **S** | `external_source`, `valuebooks_master`, `valuebooks_db` |
| **A** | `analytics_251957577`(GA4メイン), `ga_source`, `searchconsole_valuebooks`, `ad_google_valuebooks` |
| **B** | `from_marketingcloud`, `valuebooks_collabo`, `valuebooks_preservation`, `analytics_253991338`, チャリボン広告/SEO |
| **C** | Vaboo関連, 停止済み(`ecosystem`, `valuebooks_summary`, `for_bi`), YouTube, ML, NOMAD |
| **D** | `aws_etl_test`, `k2test`, `temporary`, テスト用コピー |

### analytics プロパティID対応表
| プロパティID | サイト | 更新 | 判定 |
|---|---|---|---|
| `251957577` | VBメインサイト | 毎日 | A |
| `253991338` | 第2プロパティ | 毎日 | B |
| `254019333` | 第3プロパティ | 毎日 | C（要確認） |
| `297626101` | 第4プロパティ（平日のみ=NOMAD?） | 毎日 | C |### searchconsole 鮮度確認
- `searchconsole_valuebooks`: 2026-02-24（A）
- `searchconsole_charibon`: 2026-02-24（B）
- `searchconsole_vaboo`: 2026-02-24（C → Vaboo閉鎖で停止）
