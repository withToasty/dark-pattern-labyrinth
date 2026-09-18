document.addEventListener('DOMContentLoaded',()=>{
  const section=id=>document.getElementById(id);
  const wrap=id=>section(id)?.querySelector('.portal-wrap')||section(id);
  const text=(id,sel,value)=>{const el=wrap(id)?.querySelector(sel);if(el)el.textContent=value;};
  const html=(id,sel,value)=>{const el=wrap(id)?.querySelector(sel);if(el)el.innerHTML=value;};

  // Public-facing pages should read like a real service, not like game commentary.
  const service=wrap('service');
  if(service) service.innerHTML=`
    <h2>サービスのご案内</h2>
    <p>HAPPY+会員向けの特典、ポイント、サポートサービスをご案内します。</p>
    <div class="real-list">
      <a href="#coupon"><strong>会員特典・クーポン</strong><span>会員限定の特典やキャンペーンを確認できます。</span></a>
      <a href="#points"><strong>ポイントサービス</strong><span>保有ポイントや利用状況を確認できます。</span></a>
      <a href="#faq1"><strong>サポート</strong><span>よくある質問、各種お問い合わせをご利用いただけます。</span></a>
    </div>
    <a class="btn primary" href="#jointrap">新規会員登録</a>
    <a class="tiny" href="#home">会員向けサービスTOPへ戻る</a>`;

  const join=wrap('jointrap');
  if(join) join.innerHTML=`
    <div class="form-kicker">HAPPY+ 新規会員登録</div>
    <h2>新規会員登録</h2>
    <p>メールアドレスを入力して、会員登録を開始してください。</p>
    <div class="registration-panel">
      <label class="field-label">メールアドレス</label>
      <input class="real-input" type="email" placeholder="example@email.com" aria-label="メールアドレス">
      <a class="btn primary" href="#service">登録手続きへ進む</a>
    </div>
    <a class="tiny" href="#mypage">すでに会員の方はこちら</a>
    <a class="tiny" href="#service">サービス一覧へ戻る</a>`;

  const points=wrap('points');
  if(points){
    text('points','h2','ポイント');
    const p=points.querySelector('p'); if(p)p.textContent='現在の保有ポイントは12ポイントです。有効期限を過ぎたポイントは失効し、再付与されません。';
    const primary=points.querySelector('.primary');if(primary)primary.textContent='ポイント利用履歴を確認';
    const tiny=points.querySelector('.tiny');if(tiny)tiny.textContent='マイページへ戻る';
  }

  const coupon=wrap('coupon');
  if(coupon){
    text('coupon','h2','会員特典・クーポン');
    const card=coupon.querySelector('.card');if(card)card.innerHTML='<b>HAPPY+会員限定</b><br>対象サービス 3%OFF<br><span class="sub">有効期限：2026年9月30日</span>';
    const a=coupon.querySelector('.primary');if(a)a.textContent='クーポンを表示';
  }

  const profile=wrap('profile');
  if(profile){
    const p=profile.querySelector('p');if(p)p.textContent='氏名・住所などの登録情報を確認、変更できます。契約内容は「契約・料金」からお手続きください。';
  }

  const notice=wrap('notice');
  if(notice){
    const card=notice.querySelector('.card');if(card)card.innerHTML='☑ メール通知<br>☑ プッシュ通知<br>☑ 契約・料金に関する重要なお知らせ<br>☑ キャンペーン・会員特典のお知らせ';
  }

  const upgrade=wrap('upgrade');
  if(upgrade) upgrade.innerHTML=`
    <h2>プラン変更内容の確認</h2>
    <div class="card detail-card">
      <div><span>変更後プラン</span><strong>HAPPY+ プレミアム</strong></div>
      <div><span>月額料金</span><strong>1,980円</strong></div>
      <div><span>適用日</span><strong>次回更新日から</strong></div>
    </div>
    <p class="sub">変更を確定すると、次回更新日から新しい料金が適用されます。</p>
    <a class="btn primary" href="#contract">この内容で変更する</a>
    <a class="tiny" href="#contract">変更せず契約内容へ戻る</a>`;

  const payment=wrap('payment');
  if(payment) payment.innerHTML=`
    <h2>支払い方法</h2>
    <div class="card detail-card">
      <div><span>登録カード</span><strong>VISA •••• 4821</strong></div>
      <div><span>有効期限</span><strong>08 / 29</strong></div>
    </div>
    <a class="btn ghost" href="#contract">契約・料金へ戻る</a>`;

  const receipt=wrap('receipt');
  if(receipt) receipt.innerHTML=`
    <h2>領収書</h2>
    <p>過去12か月分の領収書を確認できます。</p>
    <div class="real-list"><a href="#receipt"><strong>2026年9月分</strong><span>980円 / PDF</span></a><a href="#receipt"><strong>2026年8月分</strong><span>980円 / PDF</span></a></div>
    <a class="tiny" href="#other2">各種お手続きへ戻る</a>`;

  const namechange=wrap('namechange');
  if(namechange) namechange.innerHTML=`
    <h2>契約者名義の変更</h2>
    <p>契約者名義を変更する場合は、本人確認書類の提出が必要です。</p>
    <div class="notice-box">お手続きには通常2〜3営業日かかります。</div>
    <a class="btn ghost" href="#other2">各種お手続きへ戻る</a>`;

  text('pause','h2','会員サービスの一時休止');
  const pauseP=wrap('pause')?.querySelector('p');if(pauseP)pauseP.textContent='月額料金を0円として3か月間休止できます。休止期間終了後は自動的に通常契約へ戻ります。';
  const pausePrimary=wrap('pause')?.querySelector('.primary');if(pausePrimary)pausePrimary.textContent='3か月間休止する';
  const pauseTiny=wrap('pause')?.querySelector('.tiny');if(pauseTiny)pauseTiny.textContent='休止せず、その他のお手続きを確認する';

  const pausetrap=wrap('pausetrap');
  if(pausetrap) pausetrap.innerHTML=`
    <div class="status-success">一時休止を受け付けました</div>
    <h2>一時休止のお申し込みが完了しました</h2>
    <p>休止期間中の月額料金は0円です。3か月後に自動的に通常契約へ戻ります。</p>
    <div class="notice-box">会員契約自体は継続しています。</div>
    <a class="btn ghost" href="#other2">各種お手続きへ戻る</a>`;

  const retain=wrap('retain1');
  if(retain) retain.innerHTML=`
    <div class="status-success">お手続きが完了しました</div>
    <h2>現在の契約内容で継続します</h2>
    <p>契約内容に変更はありません。</p>
    <a class="btn ghost" href="#faqanswer">退会に関するご案内へ戻る</a>`;

  const reset=wrap('resetloop');
  if(reset) reset.innerHTML=`
    <h2>パスワード再設定</h2>
    <p>登録メールアドレス宛に、パスワード再設定用のメールを送信します。</p>
    <div class="notice-box">再設定完了後は、セキュリティ保護のためトップページから再度お手続きください。</div>
    <a class="btn primary" href="#home">再設定メールを送信する</a>
    <a class="tiny" href="#boss1">ログイン画面へ戻る</a>`;

  const b2=wrap('boss2');
  if(b2){
    const card=b2.querySelector('.card');if(card)card.innerHTML='<b>退会により利用できなくなるもの</b><br><br>・保有ポイント 12ポイント<br>・現在の会員ランク<br>・配布済みの会員限定クーポン<br>・会員限定キャンペーンへの参加資格';
  }

  text('reasontrap','h2','退会理由の詳細');
  const reasonInputs=wrap('reasontrap')?.querySelectorAll('.fake-input');
  if(reasonInputs?.length>=3){
    reasonInputs[0].textContent='退会理由の詳細（400文字以上）';
    reasonInputs[1].textContent='改善を希望する点';
    reasonInputs[2].textContent='ご連絡可能な時間帯';
  }
  const reasonBack=wrap('reasontrap')?.querySelector('.primary');if(reasonBack)reasonBack.textContent='前の画面へ戻る';

  text('boss6','h2','解約手続き');
  const b6p=wrap('boss6')?.querySelector('p');if(b6p)b6p.textContent='下記のボタンからお手続きを続けてください。';
  const b6tiny=wrap('boss6')?.querySelector('a[href="#boss7"]');if(b6tiny)b6tiny.textContent='ボタンを操作できない場合はこちら';

  const caught=wrap('runnerCaught');
  if(caught) caught.innerHTML=`
    <h2>お手続きを完了できませんでした</h2>
    <div class="notice-box">セッション情報を確認できませんでした。前の画面からもう一度お試しください。</div>
    <a class="btn primary" href="#boss6">前の画面へ戻る</a>`;

  text('boss7','h2','手続き内容の確認');
  const b7p=wrap('boss7')?.querySelector('p');if(b7p)b7p.textContent='解約を希望する場合は、下記からお手続きを続けてください。';
  const b7main=wrap('boss7')?.querySelector('a[href="#boss8"]');if(b7main)b7main.textContent='解約手続きを続ける';
  const b7tiny=wrap('boss7')?.querySelector('a[href="#wrongLearned"]');if(b7tiny)b7tiny.textContent='通知・メール配信設定を確認する';

  const wrong=wrap('wrongLearned');
  if(wrong) wrong.innerHTML=`
    <div class="status-success">設定を保存しました</div>
    <h2>通知・メール配信設定</h2>
    <p>お知らせメールの配信設定を更新しました。</p>
    <div class="notice-box">解約手続きは完了していません。</div>
    <a class="btn ghost" href="#boss7">解約手続きへ戻る</a>`;

  text('boss8','h2','解約に関するお問い合わせ');
  const b8p=wrap('boss8')?.querySelector('p');if(b8p)b8p.textContent='この契約の解約には、サポート窓口での確認が必要です。';

  text('chat1','h2','チャットサポート');
  const chat1bot=wrap('chat1')?.querySelectorAll('.bubble.bot');
  if(chat1bot?.[0])chat1bot[0].textContent='HAPPY+チャットサポートです。ご用件を選択または入力してください。';

  const chat3tiny=wrap('chat3')?.querySelector('a[href="#boss9"]');if(chat3tiny)chat3tiny.textContent='オンラインで手続きを継続する';

  const surveyCard=wrap('boss9')?.querySelector('.card');
  if(surveyCard)surveyCard.innerHTML='Q1. 退会を検討した主な理由を教えてください。<br><br>Q2. 改善を希望する点があれば教えてください。<br><br>Q3. HAPPY+を知人に勧めたいと思いますか？<br><br>Q4. 今後、サービス改善に関するご案内を希望しますか？';

  text('boss10','h2','解約内容の最終確認');
  const finalCard=wrap('boss10')?.querySelector('.card');
  if(finalCard)finalCard.innerHTML='<b>解約すると利用できなくなるもの</b><br><br>・保有ポイント 12ポイント<br>・現在の会員ランク<br>・未使用の会員限定クーポン<br>・会員向け特典・キャンペーン';
  const stay=wrap('boss10')?.querySelector('a[href="#stayfinal"]');if(stay)stay.textContent='現在の契約を継続する';
  const leave=wrap('boss10')?.querySelector('a[href="#fakeend"]');if(leave)leave.textContent='解約を確定する';

  const stayfinal=wrap('stayfinal');
  if(stayfinal){
    stayfinal.querySelector('.confetti')?.remove();
    const h=stayfinal.querySelector('h2');if(h)h.textContent='契約継続のお手続きが完了しました';
    const p=stayfinal.querySelector('p');if(p)p.textContent='現在の契約内容で継続します。';
    const a=stayfinal.querySelector('a[href="#boss10"]');if(a){a.textContent='解約手続きに戻る';a.classList.remove('primary');a.classList.add('ghost');}
  }

  const fake=wrap('fakeend');
  if(fake){
    const card=fake.querySelector('.card');if(card)card.innerHTML='<b>申請受付番号</b><br>CNL-20260918-48271';
    const a=fake.querySelector('a[href="#mail"]');if(a)a.textContent='確認メールを表示';
  }

  const mail=wrap('mail');
  if(mail){
    const h=mail.querySelector('h2');if(h)h.textContent='HAPPY+ 解約手続き確認';
    const a=mail.querySelector('a[href="#lastlogin"]');if(a)a.textContent='本人確認へ進む';
  }



  // Corporate page: real services and experimental projects give the company a believable reason to exist.
  const corp=wrap('footer');
  if(corp) corp.innerHTML=`
    <div class="corp-kicker">HAPPY PLUS, Inc.</div>
    <h2>事業・プロジェクト</h2>
    <p class="corp-lead">私たちは、日々の暮らし、都市、遊び、空間にまつわるアイデアを、小さく試し、育てています。</p>

    <div class="corp-status-guide">
      <span><i class="dot idea"></i>IDEA</span>
      <span><i class="dot research"></i>RESEARCH</span>
      <span><i class="dot prototype"></i>PROTOTYPE</span>
      <span><i class="dot building"></i>BUILDING</span>
      <span><i class="dot live"></i>LIVE</span>
    </div>

    <section class="corp-project-section">
      <div class="corp-section-head"><span>DIGITAL PRODUCTS</span><h3>暮らしを軽くする、小さな道具</h3></div>
      <div class="corp-project-grid">
        <article class="corp-project-card">
          <div class="corp-project-meta"><span class="corp-status prototype">PROTOTYPE</span><span>Systems</span></div>
          <h4>Weekly Budget</h4>
          <p>週予算を「残高」として見るための軽量ウィジェット。毎日の入力を前提にせず、全体像だけを残す。</p>
          <div class="corp-project-foot">CURRENT / iPhone widget prototype</div>
        </article>
        <article class="corp-project-card">
          <div class="corp-project-meta"><span class="corp-status research">RESEARCH</span><span>Human Behavior</span></div>
          <h4>Mission Log</h4>
          <p>音声・動画・日時を残し、未来の自分が現在地を見返せる個人ログ。記録は軽く、意味づけは後から。</p>
          <div class="corp-project-foot">CURRENT / logging model research</div>
        </article>
        <article class="corp-project-card">
          <div class="corp-project-meta"><span class="corp-status building">BUILDING</span><span>Play</span></div>
          <h4>Kecak / Looper</h4>
          <p>声やリズムを重ねて、その場で音楽を組み立てるループ型の音遊び。操作そのものが演奏になる体験。</p>
          <div class="corp-project-foot">CURRENT / interaction design</div>
        </article>
      </div>
    </section>

    <section class="corp-project-section">
      <div class="corp-section-head"><span>CITIES & DATA</span><h3>街を、別の見方で読む</h3></div>
      <div class="corp-project-grid">
        <article class="corp-project-card">
          <div class="corp-project-meta"><span class="corp-status prototype">PROTOTYPE</span><span>Cities</span></div>
          <h4>City Techno</h4>
          <p>街の映像から対象物を認識し、工事音、踏切、交通、寺社など街固有の音をテクノへ変換する映像・音楽実験。</p>
          <div class="corp-project-foot">CURRENT / video recognition pipeline</div>
        </article>
        <article class="corp-project-card">
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
        <article class="corp-project-card">
          <div class="corp-project-meta"><span class="corp-status building">BUILDING</span><span>Game</span></div>
          <h4>Grid Rogue</h4>
          <p>マス目を進み、敵を倒し、コインとアイテムを集めるシンプルなローグライク。少ない操作で判断が積み重なる設計。</p>
          <div class="corp-project-foot">CURRENT / web playable build</div>
        </article>
        <article class="corp-project-card">
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
        <article class="corp-project-card">
          <div class="corp-project-meta"><span class="corp-status idea">IDEA</span><span>Physical Space</span></div>
          <h4>Warehouse Gym</h4>
          <p>倉庫にラックとフリーウェイトだけを置き、車でそのまま入れる小規模ジム。運動、サウナ、読書までを一つの拠点に。</p>
          <div class="corp-project-foot">CURRENT / business concept</div>
        </article>
        <article class="corp-project-card">
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

    <a class="tiny sneaky corp-hidden-route" href="#mypage">会員情報の変更・その他お手続き</a>`;

  const homeFooter=document.querySelector('#home .footer-columns>div:last-child');
  if(homeFooter && !homeFooter.textContent.includes('事業・プロジェクト')){
    const a=document.createElement('a');a.href='#footer';a.textContent='事業・プロジェクト';homeFooter.prepend(a);
  }

  // FAQ explains cancellation but deliberately does not expose the actual application entrance.
  const faq=wrap('faq1');
  if(faq) faq.innerHTML=`
    <h2>よくある質問</h2>
    <p>よくお問い合わせいただく内容をご案内します。</p>
    <div class="real-list">
      <a href="#faq1"><strong>料金・請求について</strong><span>月額料金、請求日、明細の確認方法</span></a>
      <a href="#faq1"><strong>ポイント・会員特典について</strong><span>ポイントの有効期限、クーポンの利用方法</span></a>
      <a href="#resetloop"><strong>ログイン・パスワードについて</strong><span>パスワードを忘れた場合のお手続き</span></a>
      <a href="#faqanswer"><strong>退会・解約について</strong><span>退会前の確認事項とご案内</span></a>
    </div>
    <a class="tiny" href="#home">会員向けサービスTOPへ戻る</a>`;

  const faqanswer=wrap('faqanswer');
  if(faqanswer) faqanswer.innerHTML=`
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
    <a class="tiny" href="#faq1">よくある質問へ戻る</a>`;

  // Remove leftover game/meta labels from the service UI.
  document.querySelectorAll('.immersive .sub').forEach(el=>{
    if(/STEP\s*\d|WORLD|BOSS|YOU FOUND|HAPPY\+ SUPPORT|FAQ ARTICLE|MAIL/i.test(el.textContent))el.remove();
  });
});