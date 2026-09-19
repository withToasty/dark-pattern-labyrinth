document.addEventListener('DOMContentLoaded',()=>{
  const SUPABASE_URL='https://pzqpfukhfezhegfzrjke.supabase.co';
  const SUPABASE_KEY='sb_publishable_FOXFf_LV9tZClcXSfjtXGg_3KQhJcT4';
  const API=SUPABASE_URL+'/rest/v1';
  const baseHeaders={apikey:SUPABASE_KEY,'Content-Type':'application/json'};

  const fmt=(ms)=>{const cs=Math.max(0,Math.round(ms/10));const m=Math.floor(cs/6000);const s=Math.floor((cs%6000)/100);const c=cs%100;return m?`${m}:${String(s).padStart(2,'0')}.${String(c).padStart(2,'0')}`:`${s}.${String(c).padStart(2,'0')}s`;};

  async function loadTop10(){
    const url=API+'/leaderboard?select=player_name,time_ms,traps,created_at&order=time_ms.asc,created_at.asc&limit=10';
    const r=await fetch(url,{headers:{apikey:SUPABASE_KEY}});
    if(!r.ok)throw new Error('ranking fetch failed');
    return r.json();
  }

  async function getRank(timeMs){
    const r=await fetch(API+'/rpc/rank_for_score',{method:'POST',headers:baseHeaders,body:JSON.stringify({score_ms:timeMs})});
    if(!r.ok)throw new Error('rank fetch failed');
    return Number(await r.json());
  }

  function renderRows(rows,host){
    host.replaceChildren();
    if(!rows.length){const e=document.createElement('div');e.className='lb-empty';e.textContent='まだ記録がありません。最初の記録を残せます。';host.appendChild(e);return;}
    rows.forEach((row,i)=>{
      const item=document.createElement('div');item.className='lb-row'+(i===0?' lb-first':'');
      const rank=document.createElement('span');rank.className='lb-rank';rank.textContent=String(i+1);
      const name=document.createElement('span');name.className='lb-name';name.textContent=row.player_name;
      const time=document.createElement('span');time.className='lb-time';time.textContent=fmt(row.time_ms);
      item.append(rank,name,time);host.appendChild(item);
    });
  }

  async function refreshBoard(host){
    try{renderRows(await loadTop10(),host);}catch(e){host.textContent='ランキングを読み込めませんでした。';}
  }

  function mount(result){
    const end=document.getElementById('trueend');
    const resultPanel=end?.querySelector('.result-panel');
    if(!end||!resultPanel)return;
    end.querySelector('.leaderboard-panel')?.remove();

    const panel=document.createElement('section');panel.className='leaderboard-panel';
    panel.innerHTML='<div class="lb-eyebrow">WORLD RECORD</div><div class="lb-head"><div><h2>最速で脱出した人たち</h2><p>クリアタイムを世界ランキングに残せます。</p></div><div class="lb-yourtime"></div></div><div class="lb-board" aria-live="polite"><div class="lb-empty">ランキングを読み込み中…</div></div><div class="lb-submit"><label for="player-name">PLAYER NAME</label><div class="lb-form"><input id="player-name" maxlength="20" autocomplete="nickname" placeholder="名前を入力"/><button type="button">ランキングに登録</button></div><div class="lb-status" aria-live="polite"></div></div>';
    resultPanel.after(panel);
    panel.querySelector('.lb-yourtime').textContent='YOUR TIME '+fmt(result.timeMs);
    const board=panel.querySelector('.lb-board');
    refreshBoard(board);

    const input=panel.querySelector('input');const btn=panel.querySelector('button');const status=panel.querySelector('.lb-status');
    const alreadySubmitted=sessionStorage.getItem('dp-run-submitted')==='1';
    if(result.validRun===false){
      input.disabled=true;btn.disabled=true;btn.textContent='ランキング対象外';
      status.textContent='ランキング登録は、最初の画面から開始してクリアした記録のみ対象です。';
    }else if(alreadySubmitted){
      input.disabled=true;btn.disabled=true;btn.textContent='登録済み';
      status.textContent='このプレイの記録は登録済みです。';
    }
    btn.addEventListener('click',async()=>{if(result.validRun===false||sessionStorage.getItem('dp-run-submitted')==='1')return;
      const name=input.value.trim();
      if(!name){status.textContent='名前を入力してください。';input.focus();return;}
      btn.disabled=true;status.textContent='記録を送信中…';
      const payload={player_name:name,time_ms:Math.round(result.timeMs),traps:result.traps,views:result.views,revisits:result.revisits};
      try{
        const r=await fetch(API+'/leaderboard',{method:'POST',headers:{...baseHeaders,Prefer:'return=minimal'},body:JSON.stringify(payload)});
        if(!r.ok)throw new Error(await r.text());
        const rank=await getRank(payload.time_ms);
        status.textContent=`記録しました。現在 ${rank}位です。`;
        sessionStorage.setItem('dp-run-submitted','1');input.disabled=true;btn.disabled=true;btn.textContent='登録済み';
        await refreshBoard(board);
      }catch(e){
        status.textContent='送信できませんでした。少し待ってもう一度試してください。';
        btn.disabled=false;
      }
    });
  }

  window.addEventListener('dp:finished',e=>mount(e.detail));
});
