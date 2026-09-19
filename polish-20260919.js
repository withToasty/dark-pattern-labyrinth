document.addEventListener('DOMContentLoaded',()=>{
  const visual=(type)=>({
    city:`<div class="artifact-visual artifact-photo city-real"><img src="assets/city-techno.webp" alt="City Techno concept visual"><span class="artifact-kind">CONCEPT VISUAL</span></div>`,
    budget:`<div class="artifact-visual artifact-photo budget-real"><img src="assets/weekly-budget.webp" alt="Weekly Budget working widget prototype"><span class="artifact-kind">WORKING PROTOTYPE</span></div>`,
    grid:`<div class="artifact-visual artifact-photo grid-real"><img src="assets/grid-rogue.webp" alt="Grid Rogue working game prototype"><span class="artifact-kind">WORKING PROTOTYPE</span></div>`,
    loop:`<div class="artifact-visual art-loop" aria-hidden="true"><div class="loop-ring one"></div><div class="loop-ring two"></div><div class="wave-bars">${Array.from({length:18},(_,i)=>`<i style="--h:${28+(i*17)%70}%"></i>`).join('')}</div><b>VOICE LOOP / 120 BPM</b></div>`,
    taxi:`<div class="artifact-visual art-taxi" aria-hidden="true"><span class="route a"></span><span class="route b"></span><span class="route c"></span><i class="heat h1"></i><i class="heat h2"></i><i class="heat h3"></i><i class="heat h4"></i><i class="heat h5"></i><b>DEMAND / 19:30</b></div>`,
    gym:`<div class="artifact-visual art-gym" aria-hidden="true"><span class="rack rk1"></span><span class="rack rk2"></span><span class="bay"></span><span class="car"></span><b>DRIVE-IN TRAINING BAY</b></div>`,
    log:`<div class="artifact-visual art-log" aria-hidden="true"><div class="log-time">2026 / 09 / 18</div><span class="log-line l1"></span><span class="log-line l2"></span><span class="log-line l3"></span><i class="log-dot a"></i><i class="log-dot b"></i><i class="log-dot c"></i><b>MISSION LOG / 07:42</b></div>`,
    shape:`<div class="artifact-visual art-shape" aria-hidden="true"><div class="shape-stage"><i class="shape-poly"></i><i class="shape-center"></i><span class="shape-vector"></span></div><b>CENTER OF MASS / VECTOR</b></div>`,
    pictogram:`<div class="artifact-visual art-picto" aria-hidden="true"><span>FOOD</span><span>WATER</span><span>TOILET</span><span>REST</span><i>●</i><i>▲</i><i>■</i><i>＋</i><b>POINT / COMMUNICATE</b></div>`
  }[type]||'');

  const typeFor=(title)=>{
    const t=(title||'').toLowerCase();
    if(t.includes('city techno'))return 'city';
    if(t.includes('weekly budget'))return 'budget';
    if(t.includes('grid rogue'))return 'grid';
    if(t.includes('kecak')||t.includes('looper'))return 'loop';
    if(t.includes('taxi'))return 'taxi';
    if(t.includes('warehouse'))return 'gym';
    if(t.includes('mission log'))return 'log';
    if(t.includes('shape'))return 'shape';
    if(t.includes('pictogram'))return 'pictogram';
    return '';
  };

  const artifactLabel=(type)=>({
    loop:'INTERACTION STUDY',
    taxi:'SYSTEM DIAGRAM',
    gym:'LAYOUT STUDY',
    log:'UI STUDY',
    shape:'MECHANICS STUDY',
    pictogram:'SYSTEM STUDY'
  }[type]||'');

  const decorate=(root,selector,titleSelector)=>{
    root?.querySelectorAll(selector).forEach(card=>{
      if(card.querySelector('.artifact-visual'))return;
      const title=card.querySelector(titleSelector)?.textContent?.trim();
      const type=typeFor(title);
      if(!type)return;
      card.classList.add('has-artifact');
      card.insertAdjacentHTML('afterbegin',visual(type));
      const label=artifactLabel(type);
      const media=card.querySelector('.artifact-visual');
      if(label&&media&&!media.querySelector('.artifact-kind')){
        media.insertAdjacentHTML('beforeend','<span class="artifact-kind">'+label+'</span>');
      }
    });
  };

  const home=document.getElementById('home');
  const hero=home?.querySelector('.home-page-title-inner');
  if(hero&&!hero.querySelector('.lab-hero-feature')){
    const copy=document.createElement('div');
    copy.className='lab-hero-copy';
    [...hero.children].forEach(el=>copy.appendChild(el));
    const feature=document.createElement('a');
    feature.className='lab-hero-feature';
    feature.href='#service';
    feature.innerHTML=visual('city')+'<div class="lab-feature-copy"><span>FEATURED / PROTOTYPE</span><strong>City Techno</strong><p>街の映像を認識し、その場所に帰属する音を音楽へ変換する。</p></div>';
    hero.append(copy,feature);
  }

  decorate(home,'.project-preview-grid > a','strong');
  const service=document.getElementById('service');
  decorate(service,'.corp-project-card','h4');
  const guide=service?.querySelector('.corp-status-guide');
  if(guide&&!service.querySelector('.artifact-policy')){
    guide.insertAdjacentHTML('afterend','<p class="artifact-policy"><b>ARTIFACT LABELS</b>　実画面・試作品・コンセプト画像・図解を区別して表示しています。</p>');
  }
  const corp=document.getElementById('footer');
  decorate(corp,'.corp-project-card','h4');
  const corpGuide=corp?.querySelector('.corp-status-guide');
  if(corpGuide&&!corp?.querySelector('.artifact-policy')){
    corpGuide.insertAdjacentHTML('afterend','<p class="artifact-policy"><b>ARTIFACT LABELS</b>　実画面・試作品・コンセプト画像・図解を区別して表示しています。</p>');
  }

  const serviceCrumb=service?.querySelector('.portal-breadcrumb span:last-child');
  if(serviceCrumb)serviceCrumb.textContent='事業・プロジェクト';

  const memberIds=['mypage','points','coupon','history','settings','profile','notice','contract','upgrade','payment','other','other2','receipt','namechange','pause','pausetrap','faq1','faqanswer','retain1','other3','applydoor','boss1','resetloop','boss2','closeTrap','boss3','boss4','boss5','reasontrap','boss6','runnerCaught','boss7','wrongLearned','boss8','chat1','chat2','chat3','callback','boss9','surveytrap','boss10','stayfinal','fakeend','mail','lastlogin'];
  memberIds.forEach(id=>{
    const s=document.getElementById(id); if(!s)return;
    s.classList.add('member-page');
    const wrap=s.querySelector('.portal-wrap')||s;
    if(!wrap.querySelector('.member-context')){
      const chip=document.createElement('div');
      chip.className='member-context';
      chip.textContent='HAPPY+ MEMBER SERVICE';
      wrap.prepend(chip);
    }
  });

  document.querySelectorAll('.portal-nav a').forEach(a=>{
    if(a.getAttribute('href')==='#service')a.textContent='事業・プロジェクト';
  });

  const cleanMap=new Map([
    ['あと少しです。','解約内容の確認'],
    ['画面を閉じました。','お手続きを中断しました'],
    ['もう少し詳しく教えてください。','退会理由の詳細'],
    ['待たずに続ける','オンラインで手続きを継続する'],
    ['無理','前の画面に戻る']
  ]);
  const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
  const nodes=[]; while(walker.nextNode())nodes.push(walker.currentNode);
  nodes.forEach(n=>{for(const [a,b] of cleanMap){if(n.nodeValue.includes(a))n.nodeValue=n.nodeValue.replaceAll(a,b);}});

  document.querySelectorAll('.immersive a,.immersive button,.immersive input').forEach(el=>{
    el.addEventListener('focus',()=>document.body.classList.add('keyboard-focus'),{once:true});
  });

  const updateContext=()=>{
    const id=location.hash.replace('#','')||'start';
    document.body.classList.toggle('in-member-service',memberIds.includes(id));
  };
  updateContext();
  window.addEventListener('hashchange',updateContext);
});