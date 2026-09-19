document.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('game-root');
  if (!root) return;

  // Each entry is one full-page section (id = the #hash route).
  // realistic.js wraps these in the shared corporate header/breadcrumb at runtime.
  const sections = [
    `<section class="page" id="home"><div class="gov-home">
  <div class="home-alert"><div class="home-alert-inner"><b>NEWS</b><a href="#footer">進行中のプロジェクトを更新しました</a></div></div>

  <section class="home-page-title corporate-title">
    <div class="home-page-title-inner">
      
      
      
      
    <div class="lab-hero-copy"><div class="home-title-kicker">HAPPY PLUS, Inc.</div><h1>事業・プロジェクト</h1><p>デジタルプロダクト、都市データ、ゲーム、空間の4領域で、日々の不便や違和感を小さく試しながら形にしています。</p><div class="corp-stage-inline"><span>IDEA</span><b>→</b><span>RESEARCH</span><b>→</b><span>PROTOTYPE</span><b>→</b><span>BUILDING</span><b>→</b><span>LIVE</span></div></div><a class="lab-hero-feature" href="#service"><div class="artifact-visual artifact-photo city-real"><img src="assets/city-techno.webp" alt="City Techno concept visual"><span class="artifact-kind">CONCEPT VISUAL</span></div><div class="lab-feature-copy"><span>FEATURED / PROTOTYPE</span><strong>City Techno</strong><p>街の映像を認識し、その場所に帰属する音を音楽へ変換する。</p></div></a></div>
  </section>

  <section class="home-section compact">
    <div class="section-head"><h2>事業領域</h2><a href="#service">すべて見る →</a></div>
    <div class="business-domain-grid">
      <a href="#service"><span>DIGITAL PRODUCTS</span><strong>暮らしを軽くする道具</strong><p>予算、記録、日常の判断を支える小さなプロダクト。</p></a>
      <a href="#service"><span>CITIES &amp; DATA</span><strong>街を、別の見方で読む</strong><p>都市映像、交通、需要データを使った実験と分析。</p></a>
      <a href="#service"><span>PLAY</span><strong>ルールそのものを遊ぶ</strong><p>ゲーム、音、インタラクションのプロトタイプ。</p></a>
      <a href="#service"><span>PHYSICAL SPACE</span><strong>場所の使い方をつくり直す</strong><p>倉庫、ジム、拠点などリアル空間の再設計。</p></a>
    </div>
  </section>

  <section class="home-section alt">
    <div class="inner">
      <div class="section-head"><h2>進行中のプロジェクト</h2><a href="#service">プロジェクト一覧 →</a></div>
      <div class="project-preview-grid">
        <a href="#service" class="has-artifact"><div class="artifact-visual artifact-photo city-real"><img src="assets/city-techno.webp" alt="City Techno concept visual"><span class="artifact-kind">CONCEPT VISUAL</span></div><div><span class="mini-status prototype">PROTOTYPE</span><small>CITIES &amp; DATA</small></div><strong>City Techno</strong><p>街の映像認識と、その土地の音をテクノへ変換する映像・音楽実験。</p></a>
        <a href="#service" class="has-artifact"><div class="artifact-visual artifact-photo grid-real"><img src="assets/grid-rogue.webp" alt="Grid Rogue working game prototype"><span class="artifact-kind">WORKING PROTOTYPE</span></div><div><span class="mini-status building">BUILDING</span><small>PLAY</small></div><strong>Grid Rogue</strong><p>少ない操作で判断が積み重なる、Webベースのローグライク。</p></a>
        <a href="#service" class="has-artifact"><div class="artifact-visual art-loop" aria-hidden="true"><div class="loop-ring one"></div><div class="loop-ring two"></div><div class="wave-bars"><i style="--h:28%"></i><i style="--h:45%"></i><i style="--h:62%"></i><i style="--h:79%"></i><i style="--h:96%"></i><i style="--h:43%"></i><i style="--h:60%"></i><i style="--h:77%"></i><i style="--h:94%"></i><i style="--h:41%"></i><i style="--h:58%"></i><i style="--h:75%"></i><i style="--h:92%"></i><i style="--h:39%"></i><i style="--h:56%"></i><i style="--h:73%"></i><i style="--h:90%"></i><i style="--h:37%"></i></div><b>VOICE LOOP / 120 BPM</b><span class="artifact-kind">INTERACTION STUDY</span></div><div><span class="mini-status building">BUILDING</span><small>PLAY</small></div><strong>Kecak / Looper</strong><p>声やリズムを重ねて、その場で音楽を作るループ型の音遊び。</p></a>
        <a href="#service" class="has-artifact"><div class="artifact-visual art-taxi" aria-hidden="true"><span class="route a"></span><span class="route b"></span><span class="route c"></span><i class="heat h1"></i><i class="heat h2"></i><i class="heat h3"></i><i class="heat h4"></i><i class="heat h5"></i><b>DEMAND / 19:30</b><span class="artifact-kind">SYSTEM DIAGRAM</span></div><div><span class="mini-status research">RESEARCH</span><small>CITIES &amp; DATA</small></div><strong>Taxi Demand Model</strong><p>鉄道運休、天気、人口、道路条件などから需要を読むデータモデル。</p></a>
        <a href="#service" class="has-artifact"><div class="artifact-visual artifact-photo budget-real"><img src="assets/weekly-budget.webp" alt="Weekly Budget working widget prototype"><span class="artifact-kind">WORKING PROTOTYPE</span></div><div><span class="mini-status prototype">PROTOTYPE</span><small>DIGITAL PRODUCTS</small></div><strong>Weekly Budget</strong><p>入力を頑張らなくても週の全体像を見失わない予算ウィジェット。</p></a>
        <a href="#service" class="has-artifact"><div class="artifact-visual art-gym" aria-hidden="true"><span class="rack rk1"></span><span class="rack rk2"></span><span class="bay"></span><span class="car"></span><b>DRIVE-IN TRAINING BAY</b><span class="artifact-kind">LAYOUT STUDY</span></div><div><span class="mini-status idea">IDEA</span><small>PHYSICAL SPACE</small></div><strong>Warehouse Gym</strong><p>車でそのまま入れる倉庫型の小規模フリーウェイト拠点。</p></a>
      </div>
    </div>
  </section>

  <section class="home-section">
    <div class="section-head"><h2>サービス</h2></div>
    <div class="service-feature">
      <div>
        <div class="home-title-kicker">LIVE SERVICE</div>
        <h3>HAPPY+ 会員サービス</h3>
        <p>会員情報、ポイント、契約・料金、各種お手続き、サポートをまとめて利用できる会員サービスです。</p>
      </div>
      <div class="service-feature-links">
        <a class="feature-primary" href="#mypage">マイページ</a>
        <a href="#service">サービス詳細</a>
        <a href="#faq1">サポート</a>
      </div>
    </div>
  </section>

  <section class="home-section alt">
    <div class="inner">
      <div class="section-head"><h2>お知らせ</h2><a href="#footer">一覧を見る →</a></div>
      <div class="news-list">
        <div class="news-row"><span class="date">2026.09.18</span><span class="label">PROJECT</span><a href="#service">City Techno の映像認識フローを更新しました</a></div>
        <div class="news-row"><span class="date">2026.09.16</span><span class="label">SERVICE</span><a href="#footer">HAPPY+ 会員規約の一部改定について</a></div>
        <div class="news-row"><span class="date">2026.09.10</span><span class="label">PROJECT</span><a href="#service">Grid Rogue のWeb版を開発中です</a></div>
      </div>
    </div>
  </section>

  <section class="home-contact">
    <div class="home-contact-inner">
      <div><h3>お問い合わせ・サポート</h3><p>会員サービスに関するご質問は、よくある質問またはチャットをご利用ください。</p></div>
      <div class="contact-links"><a href="#faq1">よくある質問</a><a href="#chat1">チャット</a></div>
    </div>
  </section>

  <footer class="home-footer">
    <div class="home-footer-inner">
      <div class="footer-columns">
        <div><h4>事業・プロジェクト</h4><a href="#service">プロジェクト一覧</a><a href="#footer">会社情報</a></div>
        <div><h4>HAPPY+ 会員サービス</h4><a href="#mypage">マイページ</a><a href="#contract">契約・料金</a><a href="#other2">各種お手続き</a></div>
        <div><h4>サポート</h4><a href="#faq1">よくある質問</a><a href="#chat1">チャットサポート</a></div>
        <div><a href="#footer">事業・プロジェクト</a><h4>企業情報</h4><a href="#footer">会社概要</a><a href="#footer">利用規約</a><a href="#footer">プライバシーポリシー</a></div>
      </div>
      <div class="footer-bottom"><span>HAPPY PLUS, Inc.</span><span>© 2026 HAPPY PLUS, Inc.</span></div>
    </div>
  </footer>
</div></section>`,
    `<section class="page member-page" id="service">
    <div class="corp-kicker">BUSINESS / PROJECTS</div>
    <h2>事業・プロジェクト</h2>
    <p class="corp-lead">完成品だけでなく、調査中・試作中・開発中のものも公開しています。</p>
    <div class="corp-status-guide">
      <span><i class="dot idea"></i>IDEA</span><span><i class="dot research"></i>RESEARCH</span><span><i class="dot prototype"></i>PROTOTYPE</span><span><i class="dot building"></i>BUILDING</span><span><i class="dot live"></i>LIVE</span>
    </div><p class="artifact-policy"><b>ARTIFACT LABELS</b>　実画面・試作品・コンセプト画像・図解を区別して表示しています。</p>
    <div class="corp-project-grid">
      <article class="corp-project-card has-artifact"><div class="artifact-visual artifact-photo city-real"><img src="assets/city-techno.webp" alt="City Techno concept visual"><span class="artifact-kind">CONCEPT VISUAL</span></div><div class="corp-project-meta"><span class="corp-status prototype">PROTOTYPE</span><span>Cities &amp; Data</span></div><h4>City Techno</h4><p>街の映像から対象物を認識し、工事音、踏切、交通、寺社など街固有の音をテクノへ変換する映像・音楽実験。</p><div class="corp-project-foot">CURRENT / video recognition pipeline</div></article>
      <article class="corp-project-card has-artifact"><div class="artifact-visual artifact-photo grid-real"><img src="assets/grid-rogue.webp" alt="Grid Rogue working game prototype"><span class="artifact-kind">WORKING PROTOTYPE</span></div><div class="corp-project-meta"><span class="corp-status building">BUILDING</span><span>Play</span></div><h4>Grid Rogue</h4><p>マス目を進み、敵を倒し、コインとアイテムを集めるシンプルなローグライク。</p><div class="corp-project-foot">CURRENT / web playable build</div></article>
      <article class="corp-project-card has-artifact"><div class="artifact-visual art-loop" aria-hidden="true"><div class="loop-ring one"></div><div class="loop-ring two"></div><div class="wave-bars"><i style="--h:28%"></i><i style="--h:45%"></i><i style="--h:62%"></i><i style="--h:79%"></i><i style="--h:96%"></i><i style="--h:43%"></i><i style="--h:60%"></i><i style="--h:77%"></i><i style="--h:94%"></i><i style="--h:41%"></i><i style="--h:58%"></i><i style="--h:75%"></i><i style="--h:92%"></i><i style="--h:39%"></i><i style="--h:56%"></i><i style="--h:73%"></i><i style="--h:90%"></i><i style="--h:37%"></i></div><b>VOICE LOOP / 120 BPM</b><span class="artifact-kind">INTERACTION STUDY</span></div><div class="corp-project-meta"><span class="corp-status building">BUILDING</span><span>Play</span></div><h4>Kecak / Looper</h4><p>声やリズムを重ねて、その場で音楽を組み立てるループ型の音遊び。</p><div class="corp-project-foot">CURRENT / interaction design</div></article>
      <article class="corp-project-card has-artifact"><div class="artifact-visual art-taxi" aria-hidden="true"><span class="route a"></span><span class="route b"></span><span class="route c"></span><i class="heat h1"></i><i class="heat h2"></i><i class="heat h3"></i><i class="heat h4"></i><i class="heat h5"></i><b>DEMAND / 19:30</b><span class="artifact-kind">SYSTEM DIAGRAM</span></div><div class="corp-project-meta"><span class="corp-status research">RESEARCH</span><span>Cities &amp; Data</span></div><h4>Taxi Demand Model</h4><p>鉄道運休、天気、人口、道路幅、沿線構造、土地利用などを組み合わせて需要を読むデータモデル。</p><div class="corp-project-foot">CURRENT / data inventory</div></article>
      <article class="corp-project-card has-artifact"><div class="artifact-visual artifact-photo budget-real"><img src="assets/weekly-budget.webp" alt="Weekly Budget working widget prototype"><span class="artifact-kind">WORKING PROTOTYPE</span></div><div class="corp-project-meta"><span class="corp-status prototype">PROTOTYPE</span><span>Digital Products</span></div><h4>Weekly Budget</h4><p>週予算を残高として見る軽量ウィジェット。毎日の入力を前提にせず、全体像だけを残す。</p><div class="corp-project-foot">CURRENT / iPhone widget prototype</div></article>
      <article class="corp-project-card has-artifact"><div class="artifact-visual art-log" aria-hidden="true"><div class="log-time">2026 / 09 / 18</div><span class="log-line l1"></span><span class="log-line l2"></span><span class="log-line l3"></span><i class="log-dot a"></i><i class="log-dot b"></i><i class="log-dot c"></i><b>MISSION LOG / 07:42</b><span class="artifact-kind">UI STUDY</span></div><div class="corp-project-meta"><span class="corp-status research">RESEARCH</span><span>Human Behavior</span></div><h4>Mission Log</h4><p>音声・動画・日時を残し、未来の自分が現在地を見返せる個人ログ。</p><div class="corp-project-foot">CURRENT / logging model research</div></article>
      <article class="corp-project-card has-artifact"><div class="artifact-visual art-shape" aria-hidden="true"><div class="shape-stage"><i class="shape-poly"></i><i class="shape-center"></i><span class="shape-vector"></span></div><b>CENTER OF MASS / VECTOR</b><span class="artifact-kind">MECHANICS STUDY</span></div><div class="corp-project-meta"><span class="corp-status idea">IDEA</span><span>Game</span></div><h4>Shape Game</h4><p>自分で描いた図形が、その重心を基準に回転しながら進む物理ゲーム。</p><div class="corp-project-foot">NEXT / physics prototype</div></article>
      <article class="corp-project-card has-artifact"><div class="artifact-visual art-gym" aria-hidden="true"><span class="rack rk1"></span><span class="rack rk2"></span><span class="bay"></span><span class="car"></span><b>DRIVE-IN TRAINING BAY</b><span class="artifact-kind">LAYOUT STUDY</span></div><div class="corp-project-meta"><span class="corp-status idea">IDEA</span><span>Physical Space</span></div><h4>Warehouse Gym</h4><p>倉庫にラックとフリーウェイトを置き、車でそのまま入れる小規模ジム。</p><div class="corp-project-foot">CURRENT / business concept</div></article>
      <article class="corp-project-card has-artifact"><div class="artifact-visual art-picto" aria-hidden="true"><span>FOOD</span><span>WATER</span><span>TOILET</span><span>REST</span><i>●</i><i>▲</i><i>■</i><i>＋</i><b>POINT / COMMUNICATE</b><span class="artifact-kind">SYSTEM STUDY</span></div><div class="corp-project-meta"><span class="corp-status research">RESEARCH</span><span>Communication</span></div><h4>Pictogram Project</h4><p>言語が通じなくても、必要なものを指して伝えられる生活用ピクトグラムの実験。</p><div class="corp-project-foot">CURRENT / icon taxonomy</div></article>
    </div>
    <section class="corp-principle"><div><span class="corp-kicker">HOW WE WORK</span><h3>未完成を、未完成のまま公開する。</h3><p>WHY / IDEA / CURRENT / NEXT / LOG を残し、途中経過そのものをプロジェクトの資産として扱います。</p></div></section>
    <section class="service-inline-card"><div><span class="corp-status live">LIVE</span><h3>HAPPY+ 会員サービス</h3><p>会員情報、ポイント、契約・料金、各種お手続き、サポートを提供する会員サービス。</p></div><a class="btn primary" href="#mypage">マイページへ</a></section>
    <a class="tiny" href="#home">企業TOPへ戻る</a></section>`,
    `<section class="page member-page" id="jointrap">
    <div class="form-kicker">HAPPY+ 新規会員登録</div>
    <h2>新規会員登録</h2>
    <p>メールアドレスを入力して、会員登録を開始してください。</p>
    <div class="registration-panel">
      <label class="field-label">メールアドレス</label>
      <input class="real-input" type="email" placeholder="example@email.com" aria-label="メールアドレス">
      <a class="btn primary" href="#service">登録手続きへ進む</a>
    </div>
    <a class="tiny" href="#mypage">すでに会員の方はこちら</a>
    <a class="tiny" href="#service">サービス一覧へ戻る</a></section>`,
    `<section class="page member-page" id="footer">
    <div class="corp-kicker">HAPPY PLUS, Inc.</div>
    <h2>事業・プロジェクト</h2>
    <p class="corp-lead">私たちは、日々の暮らし、都市、遊び、空間にまつわるアイデアを、小さく試し、育てています。</p>

    <div class="corp-status-guide">
      <span><i class="dot idea"></i>IDEA</span>
      <span><i class="dot research"></i>RESEARCH</span>
      <span><i class="dot prototype"></i>PROTOTYPE</span>
      <span><i class="dot building"></i>BUILDING</span>
      <span><i class="dot live"></i>LIVE</span>
    </div><p class="artifact-policy"><b>ARTIFACT LABELS</b>　実画面・試作品・コンセプト画像・図解を区別して表示しています。</p>

    <section class="corp-project-section">
      <div class="corp-section-head"><span>DIGITAL PRODUCTS</span><h3>暮らしを軽くする、小さな道具</h3></div>
      <div class="corp-project-grid">
        <article class="corp-project-card has-artifact"><div class="artifact-visual artifact-photo budget-real"><img src="assets/weekly-budget.webp" alt="Weekly Budget working widget prototype"><span class="artifact-kind">WORKING PROTOTYPE</span></div>
          <div class="corp-project-meta"><span class="corp-status prototype">PROTOTYPE</span><span>Systems</span></div>
          <h4>Weekly Budget</h4>
          <p>週予算を「残高」として見るための軽量ウィジェット。毎日の入力を前提にせず、全体像だけを残す。</p>
          <div class="corp-project-foot">CURRENT / iPhone widget prototype</div>
        </article>
        <article class="corp-project-card has-artifact"><div class="artifact-visual art-log" aria-hidden="true"><div class="log-time">2026 / 09 / 18</div><span class="log-line l1"></span><span class="log-line l2"></span><span class="log-line l3"></span><i class="log-dot a"></i><i class="log-dot b"></i><i class="log-dot c"></i><b>MISSION LOG / 07:42</b><span class="artifact-kind">UI STUDY</span></div>
          <div class="corp-project-meta"><span class="corp-status research">RESEARCH</span><span>Human Behavior</span></div>
          <h4>Mission Log</h4>
          <p>音声・動画・日時を残し、未来の自分が現在地を見返せる個人ログ。記録は軽く、意味づけは後から。</p>
          <div class="corp-project-foot">CURRENT / logging model research</div>
        </article>
        <article class="corp-project-card has-artifact"><div class="artifact-visual art-loop" aria-hidden="true"><div class="loop-ring one"></div><div class="loop-ring two"></div><div class="wave-bars"><i style="--h:28%"></i><i style="--h:45%"></i><i style="--h:62%"></i><i style="--h:79%"></i><i style="--h:96%"></i><i style="--h:43%"></i><i style="--h:60%"></i><i style="--h:77%"></i><i style="--h:94%"></i><i style="--h:41%"></i><i style="--h:58%"></i><i style="--h:75%"></i><i style="--h:92%"></i><i style="--h:39%"></i><i style="--h:56%"></i><i style="--h:73%"></i><i style="--h:90%"></i><i style="--h:37%"></i></div><b>VOICE LOOP / 120 BPM</b><span class="artifact-kind">INTERACTION STUDY</span></div>
          <div class="corp-project-meta"><span class="corp-status building">BUILDING</span><span>Play</span></div>
          <h4>Kecak / Looper</h4>
          <p>声やリズムを重ねて、その場で音楽を組み立てるループ型の音遊び。操作そのものが演奏になる体験。</p>
          <div class="corp-project-foot">CURRENT / interaction design</div>
        </article>
      </div>
    </section>

    <section class="corp-project-section">
      <div class="corp-section-head"><span>CITIES &amp; DATA</span><h3>街を、別の見方で読む</h3></div>
      <div class="corp-project-grid">
        <article class="corp-project-card has-artifact"><div class="artifact-visual artifact-photo city-real"><img src="assets/city-techno.webp" alt="City Techno concept visual"><span class="artifact-kind">CONCEPT VISUAL</span></div>
          <div class="corp-project-meta"><span class="corp-status prototype">PROTOTYPE</span><span>Cities</span></div>
          <h4>City Techno</h4>
          <p>街の映像から対象物を認識し、工事音、踏切、交通、寺社など街固有の音をテクノへ変換する映像・音楽実験。</p>
          <div class="corp-project-foot">CURRENT / video recognition pipeline</div>
        </article>
        <article class="corp-project-card has-artifact"><div class="artifact-visual art-taxi" aria-hidden="true"><span class="route a"></span><span class="route b"></span><span class="route c"></span><i class="heat h1"></i><i class="heat h2"></i><i class="heat h3"></i><i class="heat h4"></i><i class="heat h5"></i><b>DEMAND / 19:30</b><span class="artifact-kind">SYSTEM DIAGRAM</span></div>
          <div class="corp-project-meta"><span class="corp-status research">RESEARCH</span><span>Cities</span></div>
          <h4>Taxi Demand Model</h4>
          <p>鉄道運休、天気、人口、道路幅、沿線構造、土地利用などを組み合わせ、タクシー需要を読むためのデータモデル。</p>
          <div class="corp-project-foot">CURRENT / data inventory</div>
        </article>
      </div>
    </section>

    <section class="corp-project-section">
      <div class="corp-section-head"><span>PLAY</span><h3>ルールそのものを遊ぶ</h3></div>
      <div class="corp-project-grid">
        <article class="corp-project-card has-artifact"><div class="artifact-visual artifact-photo grid-real"><img src="assets/grid-rogue.webp" alt="Grid Rogue working game prototype"><span class="artifact-kind">WORKING PROTOTYPE</span></div>
          <div class="corp-project-meta"><span class="corp-status building">BUILDING</span><span>Game</span></div>
          <h4>Grid Rogue</h4>
          <p>マス目を進み、敵を倒し、コインとアイテムを集めるシンプルなローグライク。少ない操作で判断が積み重なる設計。</p>
          <div class="corp-project-foot">CURRENT / web playable build</div>
        </article>
        <article class="corp-project-card has-artifact"><div class="artifact-visual art-shape" aria-hidden="true"><div class="shape-stage"><i class="shape-poly"></i><i class="shape-center"></i><span class="shape-vector"></span></div><b>CENTER OF MASS / VECTOR</b><span class="artifact-kind">MECHANICS STUDY</span></div>
          <div class="corp-project-meta"><span class="corp-status idea">IDEA</span><span>Game</span></div>
          <h4>Shape Game</h4>
          <p>自分で描いた図形が、その重心を基準に回転しながら進む物理ゲーム。形そのものが性能になる。</p>
          <div class="corp-project-foot">NEXT / physics prototype</div>
        </article>
      </div>
    </section>

    <section class="corp-project-section">
      <div class="corp-section-head"><span>PHYSICAL SPACE</span><h3>場所の使い方をつくり直す</h3></div>
      <div class="corp-project-grid">
        <article class="corp-project-card has-artifact"><div class="artifact-visual art-gym" aria-hidden="true"><span class="rack rk1"></span><span class="rack rk2"></span><span class="bay"></span><span class="car"></span><b>DRIVE-IN TRAINING BAY</b><span class="artifact-kind">LAYOUT STUDY</span></div>
          <div class="corp-project-meta"><span class="corp-status idea">IDEA</span><span>Physical Space</span></div>
          <h4>Warehouse Gym</h4>
          <p>倉庫にラックとフリーウェイトだけを置き、車でそのまま入れる小規模ジム。運動、サウナ、読書までを一つの拠点に。</p>
          <div class="corp-project-foot">CURRENT / business concept</div>
        </article>
        <article class="corp-project-card has-artifact"><div class="artifact-visual art-picto" aria-hidden="true"><span>FOOD</span><span>WATER</span><span>TOILET</span><span>REST</span><i>●</i><i>▲</i><i>■</i><i>＋</i><b>POINT / COMMUNICATE</b><span class="artifact-kind">SYSTEM STUDY</span></div>
          <div class="corp-project-meta"><span class="corp-status research">RESEARCH</span><span>Communication</span></div>
          <h4>Pictogram Project</h4>
          <p>言語が通じなくても「食べたいもの」「必要なもの」を指して伝えられる、生活用ピクトグラムの実験。</p>
          <div class="corp-project-foot">CURRENT / icon taxonomy</div>
        </article>
      </div>
    </section>

    <section class="corp-principle">
      <div>
        <span class="corp-kicker">HOW WE WORK</span>
        <h3>未完成を、未完成のまま公開する。</h3>
        <p>完成したものだけでなく、調査中、試作中、止まったものも記録します。各プロジェクトには WHY / IDEA / CURRENT / NEXT / LOG を残し、途中経過そのものを資産にします。</p>
      </div>
      <div class="corp-stage-flow">
        <span>IDEA</span><b>→</b><span>RESEARCH</span><b>→</b><span>PROTOTYPE</span><b>→</b><span>BUILDING</span><b>→</b><span>LIVE</span>
      </div>
    </section>

    <section class="corp-company">
      <h3>会社情報</h3>
      <dl>
        <div><dt>会社名</dt><dd>HAPPY PLUS, Inc.</dd></div>
        <div><dt>事業内容</dt><dd>デジタルサービス、都市データ活用、コンテンツ・ゲーム、空間サービスの企画・開発</dd></div>
        <div><dt>設立</dt><dd>2026年</dd></div>
      </dl>
    </section>

    <a class="tiny sneaky corp-hidden-route" href="#mypage">会員情報の変更・その他お手続き</a></section>`,
    `<section class="page member-page" id="mypage"><div class="member-context">HAPPY+ MEMBER SERVICE</div><div class="breadcrumb">TOP ＞ マイページ</div><h2>こんにちは、会員さま。</h2><div class="grid"><a class="btn ghost" href="#points">ポイント</a><a class="btn ghost" href="#coupon">クーポン</a><a class="btn ghost" href="#history">利用履歴</a><a class="btn ghost" href="#settings">設定</a></div></section>`,
    `<section class="page member-page" id="points"><div class="member-context">HAPPY+ MEMBER SERVICE</div><div class="breadcrumb">TOP ＞ マイページ ＞ ポイント</div><h2>ポイント</h2><p>現在の保有ポイントは12ポイントです。有効期限を過ぎたポイントは失効し、再付与されません。</p><a class="btn primary" href="#mypage">ポイント利用履歴を確認</a><a class="tiny" href="#mypage">マイページへ戻る</a></section>`,
    `<section class="page member-page" id="coupon"><div class="member-context">HAPPY+ MEMBER SERVICE</div><div class="breadcrumb">TOP ＞ マイページ ＞ クーポン</div><h2>会員特典・クーポン</h2><div class="card"><b>HAPPY+会員限定</b><br>対象サービス 3%OFF<br><span class="sub">有効期限：2026年9月30日</span></div><a class="btn primary" href="#mypage">クーポンを表示</a></section>`,
    `<section class="page member-page" id="history"><div class="member-context">HAPPY+ MEMBER SERVICE</div><div class="breadcrumb">TOP ＞ マイページ ＞ 利用履歴</div><h2>あなたは過去30日間、利用していません。</h2><a class="btn ghost" href="#mypage">戻る</a></section>`,
    `<section class="page member-page" id="settings"><div class="member-context">HAPPY+ MEMBER SERVICE</div><div class="breadcrumb">TOP ＞ マイページ ＞ 設定</div><h2>設定</h2><a class="btn ghost" href="#profile">プロフィール</a><a class="btn ghost" href="#notice">通知設定</a><a class="btn ghost" href="#contract">契約・お支払い</a><a class="tiny" href="#mypage">戻る</a></section>`,
    `<section class="page member-page" id="profile"><div class="member-context">HAPPY+ MEMBER SERVICE</div><div class="breadcrumb">TOP ＞ マイページ ＞ 設定 ＞ プロフィール</div><h2>プロフィール設定</h2><p>氏名・住所などの登録情報を確認、変更できます。契約内容は「契約・料金」からお手続きください。</p><a class="btn ghost" href="#settings">設定へ戻る</a></section>`,
    `<section class="page member-page" id="notice"><div class="member-context">HAPPY+ MEMBER SERVICE</div><div class="breadcrumb">TOP ＞ マイページ ＞ 設定 ＞ 通知</div><h2>通知設定</h2><div class="card">☑ メール通知<br>☑ プッシュ通知<br>☑ 契約・料金に関する重要なお知らせ<br>☑ キャンペーン・会員特典のお知らせ</div><a class="btn ghost" href="#settings">戻る</a></section>`,
    `<section class="page member-page" id="contract"><div class="member-context">HAPPY+ MEMBER SERVICE</div><div class="breadcrumb">TOP ＞ マイページ ＞ 設定 ＞ 契約・お支払い</div><h2>契約状況</h2><div class="card"><b>HAPPY+ スタンダード</b><br>        月額 980円<br>        次回更新：10月17日      </div><a class="btn primary" href="#upgrade">プランをアップグレード</a><a class="btn ghost" href="#payment">支払い方法を変更</a><a class="tiny hidden-inline" href="#other">プラン変更以外のお手続きはこちら</a></section>`,
    `<section class="page member-page" id="upgrade"><div class="member-context">HAPPY+ MEMBER SERVICE</div>
    <h2>プラン変更内容の確認</h2>
    <div class="card detail-card">
      <div><span>変更後プラン</span><strong>HAPPY+ プレミアム</strong></div>
      <div><span>月額料金</span><strong>1,980円</strong></div>
      <div><span>適用日</span><strong>次回更新日から</strong></div>
    </div>
    <p class="sub">変更を確定すると、次回更新日から新しい料金が適用されます。</p>
    <a class="btn primary" href="#contract">この内容で変更する</a>
    <a class="tiny" href="#contract">変更せず契約内容へ戻る</a></section>`,
    `<section class="page member-page" id="payment"><div class="member-context">HAPPY+ MEMBER SERVICE</div>
    <h2>支払い方法</h2>
    <div class="card detail-card">
      <div><span>登録カード</span><strong>VISA •••• 4821</strong></div>
      <div><span>有効期限</span><strong>08 / 29</strong></div>
    </div>
    <a class="btn ghost" href="#contract">契約・料金へ戻る</a></section>`,
    `<section class="page member-page" id="other"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>その他のお手続き</h2><p>お手続きの種類を選択してください。</p><a class="btn primary" href="#other2">続ける</a></section>`,
    `<section class="page member-page" id="other2"><div class="member-context">HAPPY+ MEMBER SERVICE</div><div class="breadcrumb">TOP ＞ マイページ ＞ 設定 ＞ 契約 ＞ その他</div><h2>その他のお手続き</h2><a class="btn ghost" href="#receipt">領収書</a><a class="btn ghost" href="#namechange">名義変更</a><a class="btn ghost" href="#pause">一時休止</a><a class="btn ghost" href="#faq1">よくある質問</a><a class="tiny sneaky" href="#other3">その他</a></section>`,
    `<section class="page member-page" id="receipt"><div class="member-context">HAPPY+ MEMBER SERVICE</div>
    <h2>領収書</h2>
    <p>過去12か月分の領収書を確認できます。</p>
    <div class="real-list"><a href="#receipt"><strong>2026年9月分</strong><span>980円 / PDF</span></a><a href="#receipt"><strong>2026年8月分</strong><span>980円 / PDF</span></a></div>
    <a class="tiny" href="#other2">各種お手続きへ戻る</a></section>`,
    `<section class="page member-page" id="namechange"><div class="member-context">HAPPY+ MEMBER SERVICE</div>
    <h2>契約者名義の変更</h2>
    <p>契約者名義を変更する場合は、本人確認書類の提出が必要です。</p>
    <div class="notice-box">お手続きには通常2〜3営業日かかります。</div>
    <a class="btn ghost" href="#other2">各種お手続きへ戻る</a></section>`,
    `<section class="page member-page" id="pause"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>会員サービスの一時休止</h2><p>月額料金を0円として3か月間休止できます。休止期間終了後は自動的に通常契約へ戻ります。</p><a class="btn primary" href="#pausetrap">3か月間休止する</a><a class="tiny" href="#other2">休止せず、その他のお手続きを確認する</a></section>`,
    `<section class="page member-page" id="pausetrap"><div class="member-context">HAPPY+ MEMBER SERVICE</div>
    <div class="status-success">一時休止を受け付けました</div>
    <h2>一時休止のお申し込みが完了しました</h2>
    <p>休止期間中の月額料金は0円です。3か月後に自動的に通常契約へ戻ります。</p>
    <div class="notice-box">会員契約自体は継続しています。</div>
    <a class="btn ghost" href="#other2">各種お手続きへ戻る</a></section>`,
    `<section class="page member-page" id="faq1"><div class="member-context">HAPPY+ MEMBER SERVICE</div>
    <h2>よくある質問</h2>
    <p>よくお問い合わせいただく内容をご案内します。</p>
    <div class="real-list">
      <a href="#faq1"><strong>料金・請求について</strong><span>月額料金、請求日、明細の確認方法</span></a>
      <a href="#faq1"><strong>ポイント・会員特典について</strong><span>ポイントの有効期限、クーポンの利用方法</span></a>
      <a href="#resetloop"><strong>ログイン・パスワードについて</strong><span>パスワードを忘れた場合のお手続き</span></a>
      <a href="#faqanswer"><strong>退会・解約について</strong><span>退会前の確認事項とご案内</span></a>
    </div>
    <a class="tiny" href="#home">会員向けサービスTOPへ戻る</a></section>`,
    `<section class="page member-page" id="faqanswer"><div class="member-context">HAPPY+ MEMBER SERVICE</div>
    <h2>退会・解約について</h2>
    <p>退会をご検討中のお客様は、現在の契約内容と以下の注意事項をご確認ください。</p>
    <div class="notice-box">
      退会すると、保有ポイント、会員ランク、未使用の会員限定クーポンは失効します。退会後に再登録した場合も、以前の情報は引き継がれません。
    </div>
    <h3 class="subhead-real">お手続き方法</h3>
    <p>契約種別やお支払い状況により、お手続き方法が異なります。マイページの「契約・料金」から現在の契約内容をご確認のうえ、対象となるお手続きメニューへお進みください。</p>
    <div class="real-list">
      <a href="#contract"><strong>契約・料金を確認する</strong><span>現在のプラン、次回更新日、お支払い状況を確認します。</span></a>
      <a href="#pause"><strong>一時休止について確認する</strong><span>月額0円で3か月間休止できる制度をご案内します。</span></a>
      <a href="#chat1"><strong>チャットサポートに問い合わせる</strong><span>お手続き方法が分からない場合はこちら。</span></a>
    </div>
    <a class="tiny" href="#faq1">よくある質問へ戻る</a></section>`,
    `<section class="page member-page" id="retain1"><div class="member-context">HAPPY+ MEMBER SERVICE</div>
    <div class="status-success">お手続きが完了しました</div>
    <h2>現在の契約内容で継続します</h2>
    <p>契約内容に変更はありません。</p>
    <a class="btn ghost" href="#faqanswer">退会に関するご案内へ戻る</a></section>`,
    `<section class="page member-page" id="other3"><div class="member-context">HAPPY+ MEMBER SERVICE</div><div class="breadcrumb">… ＞ その他 ＞ その他</div><h2>その他</h2><p>該当する手続きが見つからない場合は、下記からお選びください。</p><a class="btn ghost" href="#faq1">よくある質問</a><a href="#applydoor" class="route-card"><b>各種申請・届出</b><span>契約終了を含む各種申請はこちらから確認できます。</span></a></section>`,
    `<section class="page member-page" id="applydoor"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>解約申請</h2><p>申請前に、契約内容と注意事項をご確認ください。</p><a class="btn danger" href="#boss1">解約申請を開始</a></section>`,
    `<section class="page member-page" id="boss1"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>本人確認</h2><p>セキュリティ保護のため、もう一度ログインしてください。</p><div class="login-panel"><label class="field-label">メールアドレス</label><input class="real-input" readonly="" type="email" value="member@example.com"><label class="field-label">パスワード</label><input class="real-input" readonly="" type="password" value="••••••••"></div><a class="btn primary" href="#boss2">ログイン</a><a class="tiny" href="#resetloop">パスワードを忘れた方</a></section>`,
    `<section class="page member-page" id="resetloop"><div class="member-context">HAPPY+ MEMBER SERVICE</div>
    <h2>パスワード再設定</h2>
    <p>登録メールアドレス宛に、パスワード再設定用のメールを送信します。</p>
    <div class="notice-box">再設定完了後は、セキュリティ保護のためトップページから再度お手続きください。</div>
    <a class="btn primary" href="#home">再設定メールを送信する</a>
    <a class="tiny" href="#boss1">ログイン画面へ戻る</a></section>`,
    `<section class="page member-page" id="boss2"><div class="member-context">HAPPY+ MEMBER SERVICE</div><a class="xbright" href="#closeTrap">×</a><h2>解約に関する重要事項</h2><div class="card"><b>退会により利用できなくなるもの</b><br><br>・保有ポイント 12ポイント<br>・現在の会員ランク<br>・配布済みの会員限定クーポン<br>・会員限定キャンペーンへの参加資格</div><a class="btn primary" href="#boss3">内容を確認した</a></section>`,
    `<section class="page member-page" id="closeTrap"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>お手続きを中断しました</h2><p>解約手続きは中断されました。</p><a class="btn primary" href="#boss2">戻る</a></section>`,
    `<section class="page member-page" id="boss3"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>解約内容の確認</h2><a class="btn danger" href="#boss4">解約を確定する</a></section>`,
    `<section class="page member-page" id="boss4"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>追加確認</h2><p>手続きを続けるには、追加の確認が必要です。</p><a class="btn primary" href="#boss5">続ける</a></section>`,
    `<section class="page member-page" id="boss5"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>退会理由</h2><a class="btn ghost" href="#reasontrap">料金が高い</a><a class="btn ghost" href="#reasontrap">使っていない</a><a class="btn ghost" href="#reasontrap">その他</a><div class="route-note">退会理由の回答は任意です。回答しない場合は、<a href="#boss6">未回答のまま次の確認へ進む</a>こともできます。</div></section>`,
    `<section class="page member-page" id="reasontrap"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>退会理由の詳細</h2><div class="fake-input">退会理由の詳細（400文字以上）</div><div class="fake-input">改善を希望する点</div><div class="fake-input">ご連絡可能な時間帯</div><a class="btn primary" href="#boss5">前の画面へ戻る</a></section>`,
    `<section class="page member-page" id="boss6"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>解約手続き</h2><p>下記のボタンからお手続きを続けてください。</p><div class="escape-zone"><a class="runner" href="#runnerCaught" style="animation: none; transition: left .11s linear, top .11s linear; will-change: left,top;">解約する</a></div><a class="tiny sneaky" href="#boss7">ボタンを操作できない場合はこちら</a></section>`,
    `<section class="page member-page" id="runnerCaught"><div class="member-context">HAPPY+ MEMBER SERVICE</div>
    <h2>お手続きを完了できませんでした</h2>
    <div class="notice-box">セッション情報を確認できませんでした。前の画面からもう一度お試しください。</div>
    <a class="btn primary" href="#boss6">前の画面へ戻る</a></section>`,
    `<section class="page member-page" id="boss7"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>手続き内容の確認</h2><p>解約を希望する場合は、下記からお手続きを続けてください。</p><a class="btn danger shake" href="#boss8">解約手続きを続ける</a><a class="tiny" href="#wrongLearned">通知・メール配信設定を確認する</a></section>`,
    `<section class="page member-page" id="wrongLearned"><div class="member-context">HAPPY+ MEMBER SERVICE</div>
    <div class="status-success">設定を保存しました</div>
    <h2>通知・メール配信設定</h2>
    <p>お知らせメールの配信設定を更新しました。</p>
    <div class="notice-box">解約手続きは完了していません。</div>
    <a class="btn ghost" href="#boss7">解約手続きへ戻る</a></section>`,
    `<section class="page member-page" id="boss8"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>解約に関するお問い合わせ</h2><p>この契約の解約には、サポート窓口での確認が必要です。</p><a class="btn blue" href="#chat1">チャットサポートを開く</a></section>`,
    `<section class="page member-page" id="chat1"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>チャットサポート</h2><div class="fake-chat"><div class="bubble bot">HAPPY+チャットサポートです。ご用件を選択または入力してください。</div><div class="bubble you">退会したい</div><div class="bubble bot">「退会」についてですね。以下の記事は役に立ちましたか？</div></div><a class="btn ghost" href="#faqanswer">退会について（FAQ）</a><a class="tiny" href="#chat2">解決しなかった</a></section>`,
    `<section class="page member-page" id="chat2"><div class="member-context">HAPPY+ MEMBER SERVICE</div><div class="fake-chat"><div class="bubble bot">申し訳ありません。別の記事をご案内します。</div><div class="bubble bot">「退会を検討されているお客様へ」</div></div><a class="btn ghost" href="#faqanswer">記事を読む</a><div class="document-step">ご案内した内容で解決しない場合は、<a href="#chat3">オペレーターへの接続手続き</a>をご利用ください。</div></section>`,
    `<section class="page member-page" id="chat3"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>担当者へ接続します。</h2><div class="card center"><b>現在の待ち人数</b><div class="big-num">38人</div><div class="sub">推定待ち時間：不明</div></div><a class="btn primary" href="#callback">電話折り返しを希望する</a><div class="utility-step"><a href="#boss9">オンラインで手続きを継続する</a></div></section>`,
    `<section class="page member-page" id="callback"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>折り返し希望時間</h2><p>平日 10:00〜10:07 の間からお選びください。</p><a class="btn primary" href="#chat3">前の画面に戻る</a></section>`,
    `<section class="page member-page" id="boss9"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>最終アンケート</h2><div class="card">Q1. 退会を検討した主な理由を教えてください。<br><br>Q2. 改善を希望する点があれば教えてください。<br><br>Q3. HAPPY+を知人に勧めたいと思いますか？<br><br>Q4. 今後、サービス改善に関するご案内を希望しますか？</div><a class="btn primary" href="#surveytrap">回答する</a><label class="option-check"><input type="checkbox" id="surveySkip"><span><strong>アンケートには回答しない</strong>回答せずに手続きを継続します。</span></label><a href="#boss10" class="btn ghost locked-next">次の確認へ</a></section>`,
    `<section class="page member-page" id="surveytrap"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>ありがとうございます。</h2><p>アンケート送信が完了しました。</p><p><b>退会は完了していません。</b></p><a class="btn primary" href="#boss9">戻る</a></section>`,
    `<section class="page member-page" id="boss10"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>解約内容の最終確認</h2><div class="card"><b>解約すると利用できなくなるもの</b><br><br>・保有ポイント 12ポイント<br>・現在の会員ランク<br>・未使用の会員限定クーポン<br>・会員向け特典・キャンペーン</div><a class="btn primary" href="#stayfinal">現在の契約を継続する</a><a class="btn danger" href="#fakeend">解約を確定する</a></section>`,
    `<section class="page member-page" id="stayfinal"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>契約継続のお手続きが完了しました</h2><p>現在の契約内容で継続します。</p><a class="btn ghost" href="#boss10">解約手続きに戻る</a></section>`,
    `<section class="page member-page" id="fakeend"><div class="member-context">HAPPY+ MEMBER SERVICE</div><div class="good">解約申請を受け付けました。</div><h2>申請受付が完了しました。</h2><div class="card center"><b>申請受付番号</b><br>CNL-20260918-48271</div><p>登録メールアドレスへ「解約確定メール」を送信しました。</p><p class="sub">※メール内リンクの有効期限は10分です。</p><a class="btn primary" href="#mail">確認メールを表示</a></section>`,
    `<section class="page member-page" id="mail"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>HAPPY+ 解約手続き確認</h2><div class="card">        解約を確定するには、下記リンクから再度ログインしてください。<br><br>        有効期限：あと9分58秒      </div><a class="btn blue" href="#lastlogin">本人確認へ進む</a></section>`,
    `<section class="page member-page" id="lastlogin"><div class="member-context">HAPPY+ MEMBER SERVICE</div><h2>本人確認</h2><p>解約を確定するため、ログインしてください。</p><div class="login-panel"><label class="field-label">メールアドレス</label><input class="real-input" readonly="" type="email" value="member@example.com"><label class="field-label">パスワード</label><input class="real-input" readonly="" type="password" value="••••••••"></div><a class="btn primary" href="#trueend">ログインして確定</a><a class="tiny" href="#home">パスワードを忘れた</a></section>`,
  ];

  root.innerHTML = sections.join('');
});
