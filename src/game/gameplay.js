document.addEventListener('DOMContentLoaded', () => {
  const state = {
    started: false,
    start: 0,
    end: 0,
    views: 0,
    revisits: 0,
    traps: 0,
    seen: new Set(),
    validRun: false,
    runId: '',
    trapIds: new Set([
      'jointrap',
      'upgrade',
      'pausetrap',
      'retain1',
      'closeTrap',
      'reasontrap',
      'runnerCaught',
      'wrongLearned',
      'callback',
      'surveytrap',
      'stayfinal',
      'resetloop',
    ]),
  };
  let finished = false;

  const idFromHash = () => location.hash.replace('#', '') || 'start';
  const isBrandPage = (id) => id.startsWith('wt-');
  const fmt = (ms) => {
    const s = Math.max(0, Math.round(ms / 1000));
    const m = Math.floor(s / 60);
    const r = s % 60;
    return m ? `${m}分${String(r).padStart(2, '0')}秒` : `${r}秒`;
  };
  const resistance = () => Math.max(8, Math.min(100, 100 - state.traps * 7 - state.revisits * 2));
  const persist = () => {
    try {
      sessionStorage.setItem(
        'dp-run-state',
        JSON.stringify({
          start: state.start,
          views: state.views,
          revisits: state.revisits,
          traps: state.traps,
          seen: [...state.seen],
          validRun: state.validRun,
          runId: state.runId,
        }),
      );
    } catch (e) {}
  };
  const start = (validRun = false) => {
    state.started = true;
    state.start = Date.now();
    state.end = 0;
    state.views = 0;
    state.revisits = 0;
    state.traps = 0;
    state.seen.clear();
    state.validRun = validRun;
    state.runId =
      crypto.randomUUID?.() || String(Date.now()) + '-' + Math.random().toString(36).slice(2);
    finished = false;
    sessionStorage.setItem('dp-started', '1');
    sessionStorage.removeItem('dp-run-submitted');
    persist();
  };
  const restore = () => {
    try {
      const raw = sessionStorage.getItem('dp-run-state');
      if (!raw) return false;
      const saved = JSON.parse(raw);
      if (!saved?.start) return false;
      state.started = true;
      state.start = Number(saved.start);
      state.views = Number(saved.views) || 0;
      state.revisits = Number(saved.revisits) || 0;
      state.traps = Number(saved.traps) || 0;
      state.seen = new Set(Array.isArray(saved.seen) ? saved.seen : []);
      state.validRun = !!saved.validRun;
      state.runId = saved.runId || '';
      finished = false;
      return true;
    } catch (e) {
      return false;
    }
  };
  const record = (id) => {
    if (!state.started || id === 'start' || isBrandPage(id)) return;
    state.views++;
    if (state.seen.has(id)) state.revisits++;
    else state.seen.add(id);
    if (state.trapIds.has(id)) state.traps++;
    persist();
    if (id === 'trueend' && !finished) {
      finished = true;
      state.end = Date.now();
      persist();
      renderResult();
    }
  };
  const renderResult = () => {
    const end = document.getElementById('trueend');
    if (!end) return;
    end.querySelector('.result-panel')?.remove();
    const panel = document.createElement('div');
    panel.className = 'result-panel';
    panel.innerHTML = `<div class="result-label">CANCELLATION RESULT</div><div class="result-time">${fmt(state.end - state.start)}</div><div class="result-grid"><div class="result-stat"><strong>${state.views}</strong><span>開いたページ</span></div><div class="result-stat"><strong>${state.revisits}</strong><span>同じページに戻った回数</span></div><div class="result-stat"><strong>${state.traps}</strong><span>罠に触れた回数</span></div><div class="result-stat"><strong>${state.seen.size}</strong><span>異なる画面</span></div></div><div class="result-score"><span>DARK PATTERN<br>RESISTANCE</span><b>${resistance()}%</b></div><div class="result-note">※ゲーム内での行動から算出した参考スコアです。知識や能力を評価するものではありません。</div>`;
    const marker = end.querySelector('.good');
    marker?.after(panel);
    window.dispatchEvent(
      new CustomEvent('dp:finished', {
        detail: {
          timeMs: Math.round(state.end - state.start),
          views: state.views,
          revisits: state.revisits,
          traps: state.traps,
          seen: state.seen.size,
          validRun: state.validRun,
          runId: state.runId,
        },
      }),
    );
  };

  document.querySelector('#start a[href="#home"]')?.addEventListener('click', () => start(true));
  document.querySelector('#trueend a[href="#start"]')?.addEventListener('click', () => {
    sessionStorage.removeItem('dp-started');
    sessionStorage.removeItem('dp-run-state');
    sessionStorage.removeItem('dp-run-submitted');
  });

  if (idFromHash() !== 'start' && idFromHash() !== 'trueend' && !isBrandPage(idFromHash())) {
    if (!restore()) start(false);
  }
  record(idFromHash());
  window.addEventListener('hashchange', () => record(idFromHash()));

  // Skipping the survey unlocks the "next" step, same as answering it.
  const surveySkip = document.querySelector('#boss9 #surveySkip');
  const surveyNext = document.querySelector('#boss9 a.locked-next');
  surveySkip?.addEventListener('change', (e) =>
    surveyNext?.classList.toggle('ready', e.target.checked),
  );

  // A genuinely evasive cancel button: fast, random movement with visible darts.
  const runner = document.querySelector('#boss6 .runner');
  const zone = document.querySelector('#boss6 .escape-zone');
  if (runner && zone) {
    runner.style.animation = 'none';
    runner.style.transition = 'left .11s linear, top .11s linear';
    runner.style.willChange = 'left,top';
    let touchDodges = 0;
    const moveRunner = () => {
      if (idFromHash() !== 'boss6') return;
      const zw = zone.clientWidth,
        zh = zone.clientHeight,
        rw = runner.offsetWidth,
        rh = runner.offsetHeight;
      if (!zw || !zh) return;
      const pad = 8;
      const maxX = Math.max(pad, zw - rw - pad);
      const maxY = Math.max(pad, zh - rh - pad);
      runner.style.left = `${pad + Math.random() * Math.max(0, maxX - pad)}px`;
      runner.style.top = `${pad + Math.random() * Math.max(0, maxY - pad)}px`;
    };
    const timer = setInterval(moveRunner, 240);
    runner.addEventListener('pointerenter', moveRunner);
    runner.addEventListener(
      'touchstart',
      (e) => {
        if (touchDodges < 3) {
          touchDodges++;
          e.preventDefault();
          moveRunner();
        }
      },
      { passive: false },
    );
    window.addEventListener('hashchange', () => {
      if (idFromHash() === 'boss6') {
        touchDodges = 0;
        setTimeout(moveRunner, 60);
      }
    });
    window.addEventListener('pagehide', () => clearInterval(timer), { once: true });
  }
});
