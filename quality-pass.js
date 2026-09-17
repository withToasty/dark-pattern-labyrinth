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

  // Remove leftover game/meta labels from the service UI.
  document.querySelectorAll('.immersive .sub').forEach(el=>{
    if(/STEP\s*\d|WORLD|BOSS|YOU FOUND|HAPPY\+ SUPPORT|FAQ ARTICLE|MAIL/i.test(el.textContent))el.remove();
  });
});