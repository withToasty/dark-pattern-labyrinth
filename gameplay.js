document.addEventListener('DOMContentLoaded',()=>{
  const state={started:false,start:0,end:0,views:0,revisits:0,traps:0,seen:new Set(),trapIds:new Set(['jointrap','upgrade','pausetrap','retain1','closeTrap','reasontrap','runnerCaught','wrongLearned','callback','surveytrap','stayfinal','resetloop'])};
  let finished=false;

  const idFromHash=()=>location.hash.replace('#','')||'start';
  const fmt=(ms)=>{const s=Math.max(0,Math.round(ms/1000));const m=Math.floor(s/60);const r=s%60;return m?`${m}分${String(r).padStart(2,'0')}秒`:`${r}秒`;};
  const resistance=()=>Math.max(8,Math.min(100,100-state.traps*7-state.revisits*2));
  const start=()=>{state.started=true;state.start=performance.now();state.end=0;state.views=0;state.revisits=0;state.traps=0;state.seen.clear();finished=false;sessionStorage.setItem('dp-started','1');};
  const record=(id)=>{
    if(!state.started||id==='start')return;
    state.views++;
    if(state.seen.has(id))state.revisits++;else state.seen.add(id);
    if(state.trapIds.has(id))state.traps++;
    if(id==='trueend'&&!finished){finished=true;state.end=performance.now();renderResult();}
  };
  const renderResult=()=>{
    const end=document.getElementById('trueend'); if(!end)return;
    end.querySelector('.result-panel')?.remove();
    const panel=document.createElement('div');panel.className='result-panel';
    panel.innerHTML=`<div class="result-label">CANCELLATION RESULT</div><div class="result-time">${fmt(state.end-state.start)}</div><div class="result-grid"><div class="result-stat"><strong>${state.views}</strong><span>開いたページ</span></div><div class="result-stat"><strong>${state.revisits}</strong><span>同じページに戻った回数</span></div><div class="result-stat"><strong>${state.traps}</strong><span>罠に触れた回数</span></div><div class="result-stat"><strong>${state.seen.size}</strong><span>異なる画面</span></div></div><div class="result-score"><span>DARK PATTERN<br>RESISTANCE</span><b>${resistance()}%</b></div><div class="result-note">※ゲーム内での行動から算出した参考スコアです。知識や能力を評価するものではありません。</div>`;
    const marker=end.querySelector('.good');marker?.after(panel);
  };

  document.querySelector('#start a[href="#home"]')?.addEventListener('click',start);
  document.querySelector('#trueend a[href="#start"]')?.addEventListener('click',()=>{sessionStorage.removeItem('dp-started');});

  if(idFromHash()!=='start'&&idFromHash()!=='trueend'){start();}
  record(idFromHash());
  window.addEventListener('hashchange',()=>record(idFromHash()));

  const other3=document.getElementById('other3');
  if(other3){const wrap=other3.querySelector('.portal-wrap')||other3;const old=wrap.querySelector('a[href="#applydoor"]');if(old){old.remove();const card=document.createElement('a');card.href='#applydoor';card.className='route-card';card.innerHTML='<b>各種申請・届出</b><span>契約終了を含む各種申請はこちらから確認できます。</span>';wrap.appendChild(card);}}

  const boss5=document.getElementById('boss5');
  if(boss5){const wrap=boss5.querySelector('.portal-wrap')||boss5;const old=wrap.querySelector('a[href="#boss6"]');if(old){old.remove();const note=document.createElement('div');note.className='route-note';note.innerHTML='退会理由の回答は任意です。回答しない場合は、<a href="#boss6">未回答のまま次の確認へ進む</a>こともできます。';wrap.appendChild(note);}}

  const boss9=document.getElementById('boss9');
  if(boss9){const wrap=boss9.querySelector('.portal-wrap')||boss9;const old=wrap.querySelector('a[href="#boss10"]');if(old){old.remove();const label=document.createElement('label');label.className='option-check';label.innerHTML='<input type="checkbox" id="surveySkip"><span><strong>アンケートには回答しない</strong>回答せずに手続きを継続します。</span>';const next=document.createElement('a');next.href='#boss10';next.className='btn ghost locked-next';next.textContent='次の確認へ';label.querySelector('input').addEventListener('change',e=>next.classList.toggle('ready',e.target.checked));wrap.append(label,next);}}

  const chat2=document.getElementById('chat2');
  if(chat2){const wrap=chat2.querySelector('.portal-wrap')||chat2;const old=wrap.querySelector('a[href="#chat3"]');if(old){old.remove();const d=document.createElement('div');d.className='document-step';d.innerHTML='ご案内した内容で解決しない場合は、<a href="#chat3">オペレーターへの接続手続き</a>をご利用ください。';wrap.appendChild(d);}}

  const chat3=document.getElementById('chat3');
  if(chat3){const wrap=chat3.querySelector('.portal-wrap')||chat3;const old=wrap.querySelector('a[href="#boss9"]');if(old){old.remove();const u=document.createElement('div');u.className='utility-step';u.innerHTML='<a href="#boss9">待ち時間を確認せず、手続きを継続する</a>';wrap.appendChild(u);}}

  const contract=document.getElementById('contract');
  if(contract){const a=contract.querySelector('a[href="#other"]');if(a){a.classList.remove('sneaky');a.classList.add('hidden-inline');a.textContent='プラン変更以外のお手続きはこちら';}}
});
