document.addEventListener('DOMContentLoaded',()=>{
const immersiveIds=['home','service','jointrap','footer','mypage','points','coupon','history','settings','profile','notice','contract','upgrade','payment','other','other2','receipt','namechange','pause','pausetrap','faq1','faqanswer','retain1','other3','applydoor','boss1','resetloop','boss2','closeTrap','boss3','boss4','boss5','reasontrap','boss6','runnerCaught','boss7','wrongLearned','boss8','chat1','chat2','chat3','callback','boss9','surveytrap','boss10','stayfinal','fakeend','mail','lastlogin'];

const pageNames={
home:'ホーム',service:'事業・プロジェクト',jointrap:'新規会員登録',footer:'企業情報',mypage:'マイページ',
points:'ポイント',coupon:'会員特典・クーポン',history:'利用履歴',settings:'各種設定',profile:'プロフィール設定',
notice:'通知設定',contract:'契約・料金',upgrade:'プラン変更',payment:'支払い方法',other:'その他のお手続き',
other2:'各種お手続き',receipt:'領収書',namechange:'名義変更',pause:'一時休止',pausetrap:'一時休止',
faq1:'よくある質問',faqanswer:'退会について',retain1:'契約確認',other3:'その他のお手続き',applydoor:'解約申請',
boss1:'本人確認',resetloop:'パスワード再設定',boss2:'重要事項の確認',closeTrap:'手続き中断',boss3:'解約内容の確認',
boss4:'追加確認',boss5:'退会理由',reasontrap:'退会理由',boss6:'解約手続き',runnerCaught:'確認画面',
boss7:'解約手続き',wrongLearned:'設定確認',boss8:'サポート',chat1:'チャットサポート',chat2:'チャットサポート',
chat3:'オペレーター接続',callback:'折り返し受付',boss9:'アンケート',surveytrap:'アンケート',
boss10:'最終確認',stayfinal:'契約継続',fakeend:'申請受付',mail:'メール確認',lastlogin:'本人確認'
};

const header=`<div class="portal-head">
  <div class="portal-utility"><div>HAPPY PLUS, Inc.</div><div class="right"><span>法人のお客さま</span><span>お知らせ</span><span>English</span><span>文字サイズ</span></div></div>
  <div class="portal-main"><div><a class="portal-logo" href="#home">HAPPY<i>+</i></a><div class="portal-tagline">Digital Products / Cities & Data / Play / Space</div></div>
    <nav class="portal-nav"><a href="#service">事業・プロジェクト</a><a href="#footer">企業情報</a><a href="#faq1">サポート</a><a href="#other2">各種お手続き</a><a class="account" href="#mypage">マイページ</a></nav>
  </div>
  <div class="portal-search"><form class="portal-search-inner portal-search-form" role="search">
    <label class="portal-search-label">サイト内検索</label>
    <input class="portal-search-input" type="search" placeholder="キーワードを入力してください" aria-label="サイト内検索">
    <button class="portal-search-btn" type="submit">検索</button>
    <div class="site-search-results" aria-live="polite"></div>
  </form></div>
</div>`;

immersiveIds.forEach(id=>{
  const s=document.getElementById(id);if(!s)return;
  s.classList.add('immersive');
  if(id==='home')return;
  const inner=s.innerHTML;
  const title=pageNames[id]||'各種お手続き';
  s.innerHTML=header+`<div class="portal-breadcrumb"><a href="#home">トップ</a><span>›</span><span>${title}</span></div><div class="portal-wrap">${inner}</div>`;
});

const home=document.getElementById('home');
if(home){
home.innerHTML=header+`
<div class="gov-home">
  <div class="home-alert"><div class="home-alert-inner"><b>NEWS</b><a href="#footer">進行中のプロジェクトを更新しました</a></div></div>

  <section class="home-page-title corporate-title">
    <div class="home-page-title-inner">
      <div class="home-title-kicker">HAPPY PLUS, Inc.</div>
      <h1>事業・プロジェクト</h1>
      <p>デジタルプロダクト、都市データ、ゲーム、空間の4領域で、日々の不便や違和感を小さく試しながら形にしています。</p>
      <div class="corp-stage-inline"><span>IDEA</span><b>→</b><span>RESEARCH</span><b>→</b><span>PROTOTYPE</span><b>→</b><span>BUILDING</span><b>→</b><span>LIVE</span></div>
    </div>
  </section>

  <section class="home-section compact">
    <div class="section-head"><h2>事業領域</h2><a href="#service">すべて見る →</a></div>
    <div class="business-domain-grid">
      <a href="#service"><span>DIGITAL PRODUCTS</span><strong>暮らしを軽くする道具</strong><p>予算、記録、日常の判断を支える小さなプロダクト。</p></a>
      <a href="#service"><span>CITIES & DATA</span><strong>街を、別の見方で読む</strong><p>都市映像、交通、需要データを使った実験と分析。</p></a>
      <a href="#service"><span>PLAY</span><strong>ルールそのものを遊ぶ</strong><p>ゲーム、音、インタラクションのプロトタイプ。</p></a>
      <a href="#service"><span>PHYSICAL SPACE</span><strong>場所の使い方をつくり直す</strong><p>倉庫、ジム、拠点などリアル空間の再設計。</p></a>
    </div>
  </section>

  <section class="home-section alt">
    <div class="inner">
      <div class="section-head"><h2>進行中のプロジェクト</h2><a href="#service">プロジェクト一覧 →</a></div>
      <div class="project-preview-grid">
        <a href="#service"><div><span class="mini-status prototype">PROTOTYPE</span><small>CITIES & DATA</small></div><strong>City Techno</strong><p>街の映像認識と、その土地の音をテクノへ変換する映像・音楽実験。</p></a>
        <a href="#service"><div><span class="mini-status building">BUILDING</span><small>PLAY</small></div><strong>Grid Rogue</strong><p>少ない操作で判断が積み重なる、Webベースのローグライク。</p></a>
        <a href="#service"><div><span class="mini-status building">BUILDING</span><small>PLAY</small></div><strong>Kecak / Looper</strong><p>声やリズムを重ねて、その場で音楽を作るループ型の音遊び。</p></a>
        <a href="#service"><div><span class="mini-status research">RESEARCH</span><small>CITIES & DATA</small></div><strong>Taxi Demand Model</strong><p>鉄道運休、天気、人口、道路条件などから需要を読むデータモデル。</p></a>
        <a href="#service"><div><span class="mini-status prototype">PROTOTYPE</span><small>DIGITAL PRODUCTS</small></div><strong>Weekly Budget</strong><p>入力を頑張らなくても週の全体像を見失わない予算ウィジェット。</p></a>
        <a href="#service"><div><span class="mini-status idea">IDEA</span><small>PHYSICAL SPACE</small></div><strong>Warehouse Gym</strong><p>車でそのまま入れる倉庫型の小規模フリーウェイト拠点。</p></a>
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
        <div><h4>企業情報</h4><a href="#footer">会社概要</a><a href="#footer">利用規約</a><a href="#footer">プライバシーポリシー</a></div>
      </div>
      <div class="footer-bottom"><span>HAPPY PLUS, Inc.</span><span>© 2026 HAPPY PLUS, Inc.</span></div>
    </div>
  </footer>
</div>`}

const searchIndex=[
{title:'City Techno',desc:'街の映像認識と音を組み合わせる映像・音楽プロジェクト。',href:'#service',words:['city techno','街','テクノ','映像','画像認識']},
{title:'Grid Rogue',desc:'Webベースのローグライクゲーム。',href:'#service',words:['grid rogue','ゲーム','ローグライク']},
{title:'Kecak / Looper',desc:'声やリズムを重ねるループ型の音楽プロジェクト。',href:'#service',words:['kecak','looper','ケチャ','ルーパー','音楽','ループ']},
{title:'Taxi Demand Model',desc:'鉄道運休や天気などからタクシー需要を読むデータモデル。',href:'#service',words:['taxi','タクシー','需要','鉄道運休','天気']},
{title:'Warehouse Gym',desc:'車で入れる倉庫型トレーニング拠点の構想。',href:'#service',words:['warehouse','gym','倉庫','ジム','トレーニング']},
{title:'Mission Log',desc:'音声・動画・日時を残す個人ログの研究。',href:'#service',words:['mission log','ログ','記録','音声','動画']},
{title:'Shape Game',desc:'描いた図形の重心を使って進む物理ゲーム。',href:'#service',words:['shape','図形','重心','物理','ゲーム']},
{title:'Pictogram Project',desc:'言葉がなくても必要なことを指して伝えるピクトグラム実験。',href:'#service',words:['pictogram','ピクトグラム','アイコン','コミュニケーション']},
{title:'Weekly Budget',desc:'週単位の予算管理ウィジェット。',href:'#service',words:['weekly budget','予算','ウィジェット']},
{title:'マイページ',desc:'会員情報、利用状況、登録情報を確認できます。',href:'#mypage',words:['マイページ','会員情報','登録情報','プロフィール','住所','名前']},
{title:'契約・料金',desc:'現在の契約内容、料金、次回更新日を確認できます。',href:'#contract',words:['契約','料金','月額','プラン','更新','請求']},
{title:'支払い方法',desc:'登録済みの支払い方法を確認・変更できます。',href:'#payment',words:['支払い','決済','カード','クレジットカード','請求']},
{title:'ポイント',desc:'保有ポイントや利用状況を確認できます。',href:'#points',words:['ポイント','残高','失効']},
{title:'会員特典・クーポン',desc:'会員向け特典とクーポンを確認できます。',href:'#coupon',words:['クーポン','特典','キャンペーン']},
{title:'各種お手続き',desc:'変更・申請などの各種手続きを確認できます。',href:'#other2',words:['手続き','申請','変更','名義','領収書','休止']},
{title:'よくある質問',desc:'サービスや各種手続きに関する質問を確認できます。',href:'#faq1',words:['質問','faq','サポート','問い合わせ','困った']},
{title:'退会について',desc:'退会・解約に関する注意事項と手続き方法をご案内します。',href:'#faqanswer',words:['退会','解約','やめる','キャンセル','契約終了']}
];

function searchEntries(query){
  const q=query.trim().toLowerCase();
  if(!q)return [];
  return searchIndex
    .map(item=>({item,score:(item.title.toLowerCase().includes(q)?5:0)+item.words.reduce((s,w)=>s+(w.toLowerCase().includes(q)||q.includes(w.toLowerCase())?2:0),0)+(item.desc.toLowerCase().includes(q)?1:0)}))
    .filter(x=>x.score>0)
    .sort((a,b)=>b.score-a.score)
    .map(x=>x.item);
}

function renderSearch(form,query){
  const box=form.querySelector('.site-search-results');if(!box)return;
  box.replaceChildren();
  const q=query.trim();
  box.classList.add('open');
  if(!q){const p=document.createElement('div');p.className='search-empty';p.textContent='キーワードを入力してください。';box.appendChild(p);return;}
  const results=searchEntries(q);
  if(!results.length){const p=document.createElement('div');p.className='search-empty';p.textContent='「'+q+'」に一致するページは見つかりませんでした。';box.appendChild(p);return;}
  results.slice(0,6).forEach(item=>{
    const a=document.createElement('a');a.href=item.href;a.className='search-result';
    const strong=document.createElement('strong');strong.textContent=item.title;
    const span=document.createElement('span');span.textContent=item.desc;
    a.append(strong,span);a.addEventListener('click',()=>box.classList.remove('open'));box.appendChild(a);
  });
}

document.querySelectorAll('.portal-search-form').forEach(form=>{
  const input=form.querySelector('.portal-search-input');
  form.addEventListener('submit',e=>{e.preventDefault();renderSearch(form,input?.value||'');});
  input?.addEventListener('input',()=>{if((input.value||'').trim().length>=2)renderSearch(form,input.value);else form.querySelector('.site-search-results')?.classList.remove('open');});
});
document.addEventListener('click',e=>{document.querySelectorAll('.site-search-results.open').forEach(box=>{if(!box.parentElement.contains(e.target))box.classList.remove('open');});});

const removeTexts=['WORLD 2 / THE OTHER OTHER','YOU FOUND IT','BOSS BATTLE / 1','BOSS BATTLE / 2','HAPPY+ SUPPORT','MAIL'];
document.querySelectorAll('.sub').forEach(el=>{if(removeTexts.some(t=>el.textContent.includes(t)))el.remove();});

const replacements=new Map([
['やっとそれっぽい場所まで来ました。','お手続きの種類を選択してください。'],
['「その他」の中に、さらに「その他」があります。','該当する手続きが見つからない場合は、下記からお選びください。'],
['長かったですね。','申請前に内容をご確認ください。'],
['進捗が戻りました。','追加確認が必要です。'],
['セキュリティ上の理由です。たぶん。','セキュリティ保護のため、追加の確認を行います。'],
['下のボタンを押してください。','下の操作ボタンからお進みください。'],
['正しいものを選んでください。','手続きを続ける場合は、該当する操作を選択してください。'],
['無理','前の画面に戻る'],
['ここまでの努力はすべて無駄になりました。','継続手続きが完了しました。'],
['……まだです。','申請受付が完了しました。'],
['またです。','解約を確定するため、本人確認を行います。']
]);
const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);const nodes=[];
while(walker.nextNode())nodes.push(walker.currentNode);
nodes.forEach(n=>{for(const [a,b] of replacements){if(n.nodeValue.includes(a))n.nodeValue=n.nodeValue.replaceAll(a,b);}});
});