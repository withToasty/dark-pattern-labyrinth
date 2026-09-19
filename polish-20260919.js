document.addEventListener('DOMContentLoaded',()=>{
  const visual=(type)=>({
    city:`<div class="artifact-visual art-city" aria-hidden="true"><div class="city-glow"></div><span class="city-road r1"></span><span class="city-road r2"></span><span class="detect d1"><i>car 0.92</i></span><span class="detect d2"><i>person 0.88</i></span><span class="detect d3"><i>bus 0.84</i></span><span class="detect d4"><i>signal 0.78</i></span><b>CITY / AUDIO OBJECT MAP</b></div>`,
    budget:`<div class="artifact-visual art-budget" aria-hidden="true"><div class="budget-top">9/14〜9/20　今週あと</div><strong>9,200円</strong><div class="budget-sub">支出 800円　/　繰越 0円</div><div class="budget-days"><span>月<em>—</em></span><span>火<em>800</em></span><span>水<em>—</em></span><span>木<em>—</em></span><span>金<em>—</em></span><span>土<em>—</em></span><span>日<em>—</em></span></div><small>タップで支出追加・NMD</small></div>`,
    grid:`<div class="artifact-visual art-grid" aria-hidden="true"><span class="grid-player"></span><span class="grid-enemy e1"></span><span class="grid-enemy e2"></span><span class="grid-coin c1"></span><span class="grid-coin c2"></span><b>RUN 014 / FLOOR 03</b></div>`,
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

  const decorate=(root,selector,titleSelector)=>{
    root?.querySelectorAll(selector).forEach(card=>{
      if(card.querySelector('.artifact-visual'))return;
      const title=card.querySelector(titleSelector)?.textContent?.trim();
      const type=typeFor(title);
      if(!type)return;
      card.classList.add('has-artifact');
      card.insertAdjacentHTML('afterbegin',visual(type));
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
  const corp=document.getElementById('footer');
  decorate(corp,'.corp-project-card','h4');

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