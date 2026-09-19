document.addEventListener('DOMContentLoaded', () => {
  const layer = document.getElementById('wt-layer');
  if (!layer) return;

  // status: idea -> experiment -> making -> done (drives the 4-dot indicator)
  const STATUS_ORDER = ['idea', 'experiment', 'making', 'done'];
  const STATUS_LABEL = { idea: 'IDEA', experiment: 'EXPERIMENT', making: 'MAKING', done: 'DONE' };

  const PROJECTS = [
    {
      id: 'cancel-game',
      title: '解約できません。2',
      field: 'GAME / SATIRE',
      status: 'done',
      desc: 'ダークパターンだらけの企業サイトから、本当に退会できるまで彷徨うブラウザゲーム。笑えるけど、実際にあります。',
      ingredients: ['UX Writing', 'Dark Patterns', 'Game Design', 'Vanilla JS'],
      href: '#start',
      playable: true,
    },
    {
      id: 'random-roguelike',
      title: 'ランダム移動ローグライク（仮）',
      field: 'GAME',
      status: 'making',
      desc: '移動方向がランダムに決まる、運と判断が入り混じるダンジョン探索ローグライク。ドット絵とスロット風の戦闘演出を自作中。',
      ingredients: ['Roguelike', 'Pixel Art', 'Game Design', 'Vanilla JS'],
    },
    {
      id: 'grid-rogue',
      title: 'Grid Rogue',
      field: 'PLAY',
      status: 'making',
      desc: 'マス目を進み、敵を倒し、コインとアイテムを集めるシンプルなローグライク。少ない操作で判断が積み重なる設計。',
      ingredients: ['Roguelike', 'Web', 'Game Design'],
      image: 'assets/grid-rogue.webp',
    },
    {
      id: 'weekly-budget',
      title: 'Weekly Budget',
      field: 'DIGITAL PRODUCTS',
      status: 'making',
      desc: '週予算を「残高」として見るための軽量iPhoneウィジェット。毎日の入力を前提にせず、全体像だけを残す。',
      ingredients: ['iOS Widget', 'Personal Finance', 'Minimal UI'],
      image: 'assets/weekly-budget.webp',
    },
    {
      id: 'city-techno',
      title: 'City Techno',
      field: 'CITIES & DATA',
      status: 'experiment',
      desc: '街の映像から対象物を認識し、工事音、踏切、交通、寺社など街固有の音をテクノへ変換する映像・音楽実験。',
      ingredients: ['Video', 'Computer Vision', 'Techno', 'Tokyo'],
      image: 'assets/city-techno.webp',
    },
    {
      id: 'taxi-demand',
      title: 'Taxi Demand Model',
      field: 'CITIES & DATA',
      status: 'experiment',
      desc: '鉄道運休、天気、人口、道路幅、沿線構造、土地利用などを組み合わせてタクシー需要を読むデータモデル。',
      ingredients: ['Data', 'Transit', 'Weather', 'Urban Planning'],
    },
    {
      id: 'mission-log',
      title: 'Mission Log',
      field: 'HUMAN BEHAVIOR',
      status: 'experiment',
      desc: '音声・動画・日時を残し、未来の自分が現在地を見返せる個人ログ。記録は軽く、意味づけは後から。',
      ingredients: ['Audio', 'Video', 'Personal Archive'],
    },
    {
      id: 'pictogram',
      title: 'Pictogram Project',
      field: 'COMMUNICATION',
      status: 'experiment',
      desc: '言語が通じなくても、必要なものを指して伝えられる生活用ピクトグラムの実験。',
      ingredients: ['Icon System', 'Communication', 'Accessibility'],
    },
    {
      id: 'kecak-looper',
      title: 'Kecak / Looper',
      field: 'PLAY',
      status: 'experiment',
      desc: '声やリズムを重ねて、その場で音楽を組み立てるループ型の音遊び。操作そのものが演奏になる体験。',
      ingredients: ['Audio Loop', 'Interaction', 'Rhythm'],
    },
    {
      id: 'shape-game',
      title: 'Shape Game',
      field: 'PLAY',
      status: 'idea',
      desc: '自分で描いた図形が、その重心を基準に回転しながら進む物理ゲーム。形そのものが性能になる。',
      ingredients: ['Physics', 'Geometry', 'Game Design'],
    },
    {
      id: 'warehouse-gym',
      title: 'Warehouse Gym',
      field: 'PHYSICAL SPACE',
      status: 'idea',
      desc: '倉庫にラックとフリーウェイトを置き、車でそのまま入れる小規模ジム。運動、サウナ、読書までを一つの拠点に。',
      ingredients: ['Physical Space', 'Fitness', 'Business Concept'],
    },
    {
      id: 'cancel-game-3',
      title: '解約できません。3（仮）',
      field: 'GAME / SATIRE',
      status: 'idea',
      desc: '次章の構想：通販・Cookie・無料体験・ソシャゲ課金。敵はあなたの行動パターンを学習する。',
      ingredients: ['Dark Patterns', 'Game Design'],
    },
  ];

  const nav = () => `
    <nav class="wt-nav">
      <a class="wt-wordmark" href="#wt-home">WITH<span class="wt-dot">.</span>TOAST</a>
      <div class="wt-nav-links">
        <a href="#wt-now-making">NOW MAKING</a>
        <a href="#wt-projects">PROJECTS</a>
        <a href="#wt-experiments">EXPERIMENTS</a>
        <a href="#wt-ideas">IDEAS</a>
        <a href="#wt-with">WITH</a>
        <a href="#wt-why">WHY TOAST?</a>
      </div>
    </nav>`;

  const footer = () => `
    <footer class="wt-footer">
      <span>WITH TOAST</span>
      <span class="wt-footer-dot" title="8.8"></span>
    </footer>`;

  const statusDots = (status) => {
    const level = STATUS_ORDER.indexOf(status);
    const dots = STATUS_ORDER.map(
      (_, i) => `<i class="${i <= level ? 'is-filled' : ''}"></i>`,
    ).join('');
    return `<span class="wt-status${status === 'done' ? ' is-done' : ''}"><span class="wt-status-dots">${dots}</span>${STATUS_LABEL[status]}</span>`;
  };

  const ingredientChips = (list) =>
    `<div class="wt-ingredients"><span class="wt-ingredients-label">INGREDIENTS</span>${list
      .map((i) => `<span class="wt-chip">${i}</span>`)
      .join('')}</div>`;

  const projectCard = (p, index) => {
    const tag = p.href ? 'a' : 'div';
    const hrefAttr = p.href ? ` href="${p.href}"` : '';
    return `
    <${tag} class="wt-card${p.playable ? ' wt-card-play' : ''}"${hrefAttr}>
      <span class="wt-card-num">${String(index + 1).padStart(2, '0')}</span>
      <div class="wt-card-head">
        <span class="wt-card-field">${p.field}</span>
      </div>
      ${statusDots(p.status)}
      <h3>${p.title}</h3>
      <p>${p.desc}</p>
      ${ingredientChips(p.ingredients)}
      ${p.playable ? '<span class="wt-card-play-cta">遊んでみる</span>' : ''}
    </${tag}>`;
  };

  const projectGrid = (list) => `<div class="wt-grid">${list.map(projectCard).join('')}</div>`;

  const byStatus = (status) => PROJECTS.filter((p) => p.status === status);
  const byStatusIn = (statuses) => PROJECTS.filter((p) => statuses.includes(p.status));

  // ---------------- WT HOME ----------------
  const wtHome = () => `
    <section class="wt-page" id="wt-home">
      ${nav()}
      <div class="wt-shell">
        <header class="wt-hero">
          <h1 class="wt-hero-mark">WITH<span class="wt-dot">.</span>TOAST</h1>
          <p class="wt-hero-jp">トースと、つくる。</p>
          <p class="wt-hero-en">Toast is the base.<br />Ideas are the toppings.</p>
          <div class="wt-hero-mix" aria-hidden="true">
            <span class="wt-hero-tag" style="--d:0s">CITY</span>
            <span class="wt-hero-tag" style="--d:1.4s">VIDEO</span>
            <span class="wt-hero-tag" style="--d:0.7s">AI</span>
            <span class="wt-hero-tag" style="--d:2.1s">TECHNO</span>
            <span class="wt-hero-tag" style="--d:2.8s">TOKYO</span>
          </div>
          <p class="wt-hero-result">
            → <b>CITY TECHNO PROJECT</b> になる。<a href="#wt-experiments" class="wt-inline-link">EXPERIMENTSで見る</a>
          </p>
        </header>

        <section class="wt-section">
          <div class="wt-section-head">
            <h2>NOW MAKING</h2>
            <a href="#wt-now-making" class="wt-inline-link">すべて見る →</a>
          </div>
          <p class="wt-section-lead">完成したものだけでなく、今まさに手を動かしているものを見せる場所です。</p>
          ${projectGrid(byStatus('making').slice(0, 2))}
        </section>
      </div>
      ${footer()}
    </section>`;

  // ---------------- NOW MAKING ----------------
  const wtNowMaking = () => `
    <section class="wt-page" id="wt-now-making">
      ${nav()}
      <div class="wt-shell">
        <section class="wt-section" style="padding-top:40px">
          <div class="wt-eyebrow">今、何を作っているか</div>
          <div class="wt-section-head" style="border:none;margin-bottom:6px;padding-bottom:0">
            <h1>NOW MAKING</h1>
          </div>
          <p class="wt-section-lead">「何を完成させたか」より、「今、何を作っているか」の方が、たぶん私たちらしい。</p>
          <div class="wt-making-list">
            ${byStatus('making')
              .map(
                (p, i) => `
              <a class="wt-making-card" href="${p.href || '#wt-projects-' + p.id}">
                <div class="wt-making-top">
                  <span class="wt-card-field">${p.field}</span>
                  ${statusDots(p.status)}
                </div>
                <h3>${p.title}</h3>
                <p>${p.desc}</p>
                ${ingredientChips(p.ingredients)}
              </a>`,
              )
              .join('')}
          </div>
        </section>
      </div>
      ${footer()}
    </section>`;

  // ---------------- PROJECTS ----------------
  const wtProjects = () => `
    <section class="wt-page" id="wt-projects">
      ${nav()}
      <div class="wt-shell">
        <section class="wt-section" style="padding-top:40px">
          <div class="wt-section-head">
            <h1>PROJECTS</h1>
          </div>
          <p class="wt-section-lead">土台の上に、実際に形になったもの。会社自体はキャンバス、プロジェクトが色を持つ。</p>
          ${projectGrid(byStatusIn(['making', 'done']))}
        </section>
      </div>
      ${footer()}
    </section>`;

  // ---------------- EXPERIMENTS ----------------
  const wtExperiments = () => `
    <section class="wt-page" id="wt-experiments">
      ${nav()}
      <div class="wt-shell">
        <section class="wt-section" style="padding-top:40px">
          <div class="wt-section-head">
            <h1>EXPERIMENTS</h1>
          </div>
          <p class="wt-section-lead">試作、小さな実験、検証。まだ何になるか分からないものたち。</p>
          ${projectGrid(byStatus('experiment'))}
        </section>
      </div>
      ${footer()}
    </section>`;

  // ---------------- IDEAS ----------------
  const wtIdeas = () => `
    <section class="wt-page" id="wt-ideas">
      ${nav()}
      <div class="wt-shell">
        <section class="wt-section" style="padding-top:40px">
          <div class="wt-section-head">
            <h1>IDEAS</h1>
          </div>
          <p class="wt-section-lead">まだ構想段階のもの。トッピングを選んでいる途中。</p>
          ${projectGrid(byStatus('idea'))}
        </section>
      </div>
      ${footer()}
    </section>`;

  // ---------------- WITH ----------------
  const wtWith = () => `
    <section class="wt-page" id="wt-with">
      ${nav()}
      <div class="wt-shell">
        <section class="wt-section" style="padding-top:40px">
          <div class="wt-section-head">
            <h1>WITH</h1>
          </div>
          <p class="wt-section-lead">「BY TOAST」ではなく「WITH TOAST」。一人で完成させるより、誰かと一緒につくりたい。</p>
          <div class="wt-with-card">
            <strong>今のところ</strong><br />
            すべてのプロジェクトは、トース（<b>Toast</b>）が一人でつくっています。
          </div>
          <div class="wt-with-card">
            <strong>これから</strong><br />
            ゲーム、映像、音楽、Web、プロダクト、研究。分野を問わず、面白そうと思ってくれたエンジニア・デザイナー・研究者・職人の方は、いつでも歓迎です。トッピングは多い方がいい。
          </div>
        </section>
      </div>
      ${footer()}
    </section>`;

  // ---------------- WHY TOAST? ----------------
  const wtWhy = () => `
    <section class="wt-page wt-why-page" id="wt-why">
      ${nav()}
      <div class="wt-why-step wt-why-lede">
        <p class="wt-why-toast">TOAST</p>
      </div>
      <div class="wt-why-step">
        <p>WITH TOASTの「Toast」は、私のあだ名「トース」から来ています。</p>
        <p>でも、この名前を気に入った理由は、それだけではありません。</p>
      </div>
      <div class="wt-why-step">
        <p>トーストは、とてもシンプルな食べ物です。</p>
        <p>そのままでも食べられる。けれど、卵を乗せてもいい。チーズでも、果物でも、アボカドでもいい。</p>
        <p>何を組み合わせるかによって、まったく違うものになる。</p>
        <div class="wt-why-toppings">
          <span>MUSIC</span><span>AI</span><span>FILM</span><span>GAME</span
          ><span>CITY</span><span>TECH</span><span>PEOPLE</span><span>RESEARCH</span>
        </div>
      </div>
      <div class="wt-why-step">
        <p>私たちがつくりたいものも、たぶんそれに近い。</p>
        <p>技術と音楽。街と映像。遊びと研究。人と人。</p>
        <p>一見関係のないものを組み合わせてみることで、まだ名前のないものが生まれる。</p>
      </div>
      <div class="wt-why-step">
        <p class="wt-why-statement"><em>Toast is the base.</em><br />Ideas are the toppings.</p>
      </div>
      <div class="wt-why-step">
        <p>WITH TOASTは、特定のジャンルだけをつくる会社ではありません。</p>
        <p>ゲーム、映像、音楽、Web、プロダクト、研究。面白いと思ったものを試し、違う分野の人たちと組み合わせながら、形にしていく場所です。</p>
      </div>
      <div class="wt-why-step">
        <p>そして、名前を「BY TOAST」ではなく「WITH TOAST」にしたのにも理由があります。</p>
        <p>一人で完成させるのではなく、トースと、一緒につくる。</p>
        <p>そんな会社でありたいと思っています。</p>
      </div>
      <div class="wt-why-step">
        <div class="wt-why-flip">
          <span class="wt-by">BY TOAST<br />トースがつくる。</span>
          <span class="wt-with">WITH TOAST<br />トースと、つくる。</span>
        </div>
      </div>
      ${footer()}
    </section>`;

  layer.innerHTML = [
    wtHome(),
    wtNowMaking(),
    wtProjects(),
    wtExperiments(),
    wtIdeas(),
    wtWith(),
    wtWhy(),
  ].join('');

  // mark current nav link
  const markCurrentNav = () => {
    const id = location.hash.replace('#', '') || 'wt-home';
    layer.querySelectorAll('.wt-nav-links a').forEach((a) => {
      a.classList.toggle('is-current', a.getAttribute('href') === '#' + id);
    });
  };
  markCurrentNav();
  window.addEventListener('hashchange', markCurrentNav);

  // reveal WHY TOAST steps as they scroll into view
  const steps = layer.querySelectorAll('.wt-why-step');
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) e.target.classList.add('is-visible');
      });
    },
    { threshold: 0.35 },
  );
  steps.forEach((s) => io.observe(s));
});
