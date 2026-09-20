# PROJECT NOTES — 解約できません。2

最終更新: 2026-09-19

## 1. このリポジトリで何を作っているか

ダークパターンを題材にした風刺・教育ゲーム「解約できません。2」。

表面上は普通の企業サイト / 会員サービスサイトに見えるが、プレイヤーはトップページから解約導線を探し、複数の妨害・誘導・ループを抜けて本当の退会完了まで進む。

ゲーム中は攻略ヒントや作者のツッコミを極力出さない。
「これは罠です」と説明せず、実在しそうなUIとして体験させる。
解説は本当に退会できた後の結果画面にまとめる。

公開URL:
https://withtoasty.github.io/dark-pattern-labyrinth/

---

## 2. 世界観

架空企業:
- 株式会社コンバージョン第一
- サービスブランド: HAPPY+
- 社是: 「顧客の意思よりKPI。」

現在は、HAPPY PLUS, Inc. の企業サイトの中に HAPPY+ 会員サービスが存在する構造。

企業側には、個人制作のアイデア / プロジェクトを事業・研究案件として掲載している。

主な掲載プロジェクト:
- City Techno
- Grid Rogue
- Weekly Budget
- Kecak / Looper
- Taxi Demand Model
- Mission Log
- Shape Game
- Warehouse Gym
- Pictogram Project

プロジェクトの状態表示:
IDEA → RESEARCH → PROTOTYPE → BUILDING → LIVE

---

## 3. UI / デザイン方針

### 企業サイト
東京都の公共サイトや大企業サイトのような、
「少し情報量が多く、事務的で、本当に存在しそう」な方向を狙う。

避けるもの:
- AI生成LPっぽい巨大キャッチコピー
- 過剰な余白
- 何でもカード化
- きれいすぎるマーケティング文
- ゲーム中のメタ台詞
- 「小さい文字を探す」などの攻略ヒント

優先するもの:
- 事務的な見出し
- サイト内検索
- パンくず
- よくある質問
- お知らせ
- 契約 / 支払い / 各種手続き
- 実在サイトにありそうな補助リンク

### 会員サービス
企業サイトから HAPPY+ の会員サービスに入っても、
別ゲーム画面に切り替わった感じを出さず、同じ企業のサービスとして自然に見せる。

---

## 4. プロジェクト画像のルール

「全部同じ絵柄」にしない。
案件に合わせて画像の種類を変え、額縁・比率・ラベルだけ統一する。

優先順位:
1. 実物がある → 実スクリーンショット
2. 実物が弱い → UIモック
3. まだ存在しない → CONCEPT VISUAL
4. 分析・仕組み → SYSTEM DIAGRAM
5. 空間構想 → LAYOUT STUDY

現在の代表例:
- Grid Rogue: WORKING PROTOTYPE（実ゲーム画面）
- Weekly Budget: WORKING PROTOTYPE（実ウィジェット）
- City Techno: CONCEPT VISUAL
- Taxi Demand Model: SYSTEM DIAGRAM
- Warehouse Gym: LAYOUT STUDY

重要:
画像がないからといって「それっぽい絵」を勝手に当てない。
意味がずれるくらいなら、図解やプレースホルダーの方を選ぶ。

---

## 5. 解約ルートの考え方

FAQから解約まで一直線にしない。

現在の思想:
- FAQは「説明」はする
- 本当の申請入口は別の階層に置く
- 正解ルートは完全不可視にはしない
- ただし、継続・アップグレード・休止・サポート等の導線より弱くする

主な導線:
企業TOP
→ マイページ
→ 設定
→ 契約・料金
→ プラン変更以外のお手続き
→ その他
→ その他
→ 各種申請
→ 解約申請
→ 本人確認
→ 注意事項
→ 退会理由
→ 移動する解約ボタン
→ サポート / チャット
→ アンケート
→ 最終確認
→ 申請受付
→ メール確認
→ 再ログイン
→ TRUE END

FAQの「退会・解約について」は、直接申請へ飛ばさず
契約・料金 / 一時休止 / チャットなどへ誘導する。

---

## 6. ダークパターンの表現ルール

ゲーム中は手法名を表示しない。

TRUE ENDで解説する主な概念:
- Obstruction / 妨害
- Misdirection / 誘導
- Roach Motel
- Interface Interference
- Forced Action
- Loop / Dead End

Fake Progress は途中で廃止。
「あと○STEP」「92%完了」などのゲーム的な進捗表現は使わない。

---

## 7. 特殊ギミック

### 移動する解約ボタン
#boss6 で本当に移動する。
CSSアニメだけではなく JS で位置をランダム変更。

現状:
- 約240msごとに移動
- pointerenter でも移動
- モバイルでは最初の数回の touch を回避

### 検索
企業サイト内検索は動作する。

検索対象例:
- City Techno
- Grid Rogue
- Weekly Budget
- Kecak / Looper
- Taxi Demand Model
- Warehouse Gym
- Mission Log
- Shape Game
- Pictogram Project
- 契約
- 料金
- 支払い
- ポイント
- 退会 / 解約

「解約」で検索しても FAQ に着く程度にし、本当の申請入口へのショートカットにはしない。

---

## 8. タイム / ランキング

Supabaseを使った WORLD RECORD 機能あり。

記録:
- player_name
- time_ms
- traps
- views
- revisits
- created_at

表示:
- TOP10
- YOUR TIME
- 登録後の現在順位

ランキングは「最初のゲーム画面から正式に開始したプレイ」のみ登録対象。
途中のハッシュURLから直接入ったプレイは対象外。

開始時刻・進行状態は sessionStorage に保持し、
ページ再読み込みによるタイマーリセットをしにくくしている。

注意:
現在はブラウザからSupabaseへ記録を送るため、
完全なチート防止にはなっていない。
本格運用するならサーバー側検証が必要。

---

## 9. 主なファイル

ルート直下にCSS/JSを並べると見通しが悪いので、`src/game/`（解約できません。2 本体）と
`src/brand/`（WITH TOASTのブランドレイヤー）に分けている。

- index.html
  - 外側のゲーム開始画面 / TRUE END
  - `src/game/*` `src/brand/*` の読み込み

- src/game/game-data.js
  - 各画面(id単位)の最終的な表示内容。1セクション = 1行のテンプレートリテラル。
  - 以前はここに書いた内容をquality-pass.js/polish.js/gameplay.js/realistic.jsが
    実行時に正規表現やquerySelectorで上書き・削除していたが、現在は最終的な表示内容を
    直接ここに書く方式に統一した（変更点はgit historyの「Consolidate 4-layer patch
    structure」コミットを参照）。

- src/game/realistic.js / realistic.css
  - 企業サイトの共通ヘッダー/パンくず/`.portal-wrap`のテンプレート化（IDリスト駆動、game-data.jsの
    各セクションを実行時にラップする）
  - サイト内検索

- src/game/gameplay.js / gameplay.css
  - タイマー / トラップ記録 / 移動ボタン / 正式ラン判定
  - アンケートのスキップ用チェックボックスの挙動（要素自体はgame-data.js側の静的HTML）
  - `wt-` で始まるIDはゲームページ扱いしない（WITH TOAST側を回遊してもタイマー等が
    誤発火しないためのガード。`isBrandPage()`）

- src/game/quality-pass.css
  - プロジェクト / 内部ページの品質調整用CSS（対応するquality-pass.jsは統合済みで削除済み）

- src/game/polish.js / polish.css
  - プロジェクトカードのアーティファクト表示、会員サービス文脈のbodyクラス切り替え、
    キーボードフォーカス時のアクセシビリティ対応（旧polish-20260919.jsをリネーム、
    内容の大部分はgame-data.jsへ統合済み）

- src/game/leaderboard.js / leaderboard.css
  - Supabase WORLD RECORD

- src/brand/brand.js / brand.css
  - WITH TOASTのブランドレイヤー本体。詳細は14章参照。

- scripts/bump-version.js
  - index.html内の全`?v=`キャッシュバスターを一括更新するヘルパー。
    `node scripts/bump-version.js [バージョン文字列]`（省略時は今日の日付）。
    ファイルを更新したら、手で書き換える代わりにこれを実行する。

- assets/
  - grid-rogue.webp
  - weekly-budget.webp
  - city-techno.webp
  - （`src/game/`・`src/brand/`どちらのJSからも`assets/...`という相対パスで参照するため、
    ルート直下のまま。index.htmlがルートにある限りこれで解決できる）

---

## 10. 現在の重要なデザイン判断

- 企業サイトとゲームを別物に見せない
- 企業として何をやっている会社か分かるようにする
- プロジェクトには可能な限り成果物を見せる
- 実物 / モック / 概念図をラベルで区別する
- ゲーム中の文章は普通のカスタマーサイトの文章にする
- 笑いは「作者のツッコミ」ではなく、企業UIの異常さそのもので出す
- 解約導線は難しくするが、単純な文字探しゲームにはしない
- ダークパターンを学習できるが、プレイ中は授業っぽくしない

---

## 11. 次に見るべき改善点

優先度高:
- iPhone実機で全ルートを通し、文字切れ・押しにくい箇所を確認
- プロジェクト画像の意味と本文の一致を都度確認
- City Techno の最終コンセプト画像を必要に応じて更新
- 各プロジェクトに個別詳細ページを作るか判断
- FAQ / チャット部分が単なる面倒さではなく「誘導」として成立しているか再レビュー
- 解約ボタンの移動速度が理不尽すぎないか実機調整

将来:
- プレイヤー行動を記録し、罠を適応させる
- 正解ルートのランダム化
- 誤操作時に大きく戻される構造
- 通販 / Cookie / 無料体験 / ガチャ / モバイル課金などの別章

---

## 12. 公開・検索について

GitHub Pagesで公開中。

robots.txt:
User-agent: *
Disallow: /

index.htmlにも noindex / nofollow 等を設定。

ただしこれは「検索されにくくする」ためのもので、
公開リポジトリやGitHub Pagesを秘密にする仕組みではない。

---

## 13. 変更時のセルフチェック

変更前後で最低限確認する:

- JavaScriptの構文エラーがないか
- スマホ幅で崩れていないか
- ゲーム中にメタ台詞が復活していないか
- FAQから解約へ近道できすぎていないか
- 実物のあるプロジェクトに架空画像を使っていないか
- プロジェクト画像と説明が一致しているか
- TRUE END以外でダークパターン名を説明していないか
- GitHub Pagesのデプロイが成功したか

---

## 14. WITH TOAST ブランドレイヤー（2026-09-20〜）

このサイトの「顔」は、`docs/WITH_TOAST_BRAND.md` を正本とするWITH TOASTのブランドサイトに変わった。
「解約できません。2」は消えておらず、WITH TOASTのPROJECTS内の1プロジェクトとして残る。

### 構造

- `src/brand/brand.css` / `src/brand/brand.js` が新設。`.wt-layer`（`id="wt-layer"`）という
  画面全体を覆う固定レイヤーの中に、WITH TOASTの各ページ（`.wt-page`、
  `id="wt-home" / "wt-now-making" / "wt-projects" / "wt-experiments" /
  "wt-ideas" / "wt-with" / "wt-why"`）をhashルーティングで表示する。
- ゲーム本体（`.app` / `#start` 以下すべて）は**無改造**。
  `.page:target` が何かにマッチした瞬間だけ `.app` が表示され、
  `.wt-layer` は自動的に隠れる（index.html内のCSSで制御）。
  何もマッチしていない（トップ訪問時）は `.wt-layer` が既定表示。
- PROJECTSページの「解約できません。2」カードから `#start` へ飛ぶと、
  今まで通りのゲーム体験（タイマー・移動する解約ボタン・リーダーボード等）に入る。
- `gameplay.js` は `wt-` で始まるIDを「ゲームのページではない」とみなし、
  WITH TOASTを回遊してもタイマーや正式ラン判定が誤発火しないようにしている
  （`isBrandPage()`）。

### プロジェクトデータ

`src/brand/brand.js` 内の `PROJECTS` 配列がNOW MAKING / PROJECTS / EXPERIMENTS / IDEASの
出し分け元。各プロジェクトは `status`（idea / experiment / making / done）を持ち、
この値でどのページに出るか、ステータスドットの表示が決まる。

### 隠し色（Anniversary Indigo #202688）の使用箇所

- プロジェクトカード右上の番号（`.wt-card-num`）
- footerの小さな点（hoverで色が変わる。`title`属性に日付のみ）

これ以上は増やさない。ブランドの主要色として使わないこと。

このファイルは、設計判断が変わったら随時更新する。
