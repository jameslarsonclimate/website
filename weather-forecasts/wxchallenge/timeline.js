/* Forecasts and observations: every 06Z-06Z day of the current city side by side, scrolling
   back in time from the day being forecast. Each day shows the runs that were out before its
   00Z deadline (the newest day's keep updating until then), today's newest runs (dotted), an
   hourly average of the models switched on, and the observations. Hovering a day shows its
   numbers in the card below the chart; a click pins it.
   The dewpoint and RH panels (below the cloud panel) are on unless the "Dewpoint & RH panels"
   button turns them off; RH is computed here from each temperature and dewpoint (the ensembles
   bring their own: the mean of their members' RH).
   The "Magnifier" button turns on a round lens that follows the pointer and shows the chart
   under it enlarged (a <use> of the chart, so it tracks the crosshair too); Esc turns it off.
   Data: ../data/wxchallenge/timeline.json, written by wxc_timeline.py (display only). */
(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const sec = $('timeline'), ctl = $('tl-controls'), wrap = $('tl-wrap'), sc = $('tl-scroll'),
        chart = $('tl-chart'), axisEl = $('tl-axis'), card = $('tl-card'),
        lens = $('tl-lens'), lensSvg = $('tl-lens-svg'), zoomBtn = $('tl-zoom');
  if (!sec || !chart) return;

  // AIFS and AIFS_ENS left out for now (6-hourly), see GRIB_ORDER in the pipeline
  const ORDER = ['HRRR', 'RRFS', 'IFS', 'IFS_HRES', 'GFS', /* 'AIFS', */ 'GFS_MOS', 'NBM', 'USL', 'ENS', /* 'AIFS_ENS', */ 'GEFS'];
  // the same colours and line styles as the static figures (matplotlib tab10)
  const COL = { HRRR: '#1f77b4', RRFS: '#bcbd22', IFS: '#ff7f0e', IFS_HRES: '#a63603', GFS: '#2ca02c', AIFS: '#d62728',
                GFS_MOS: '#2ca02c', NBM: '#8c564b', USL: '#e377c2', ENS: '#17becf', AIFS_ENS: '#d62728',
                GEFS: '#9467bd' };
  const DASHED = new Set(['GFS_MOS', 'NBM', 'USL', 'ENS', 'AIFS_ENS', 'GEFS']);
  const PRESETS = [['All', null], ['None', []], ['Deterministic', ['HRRR', 'RRFS', 'IFS', 'IFS_HRES', 'GFS' /* , 'AIFS' */]],
                   ['MOS / statistical', ['GFS_MOS', 'NBM', 'USL']], ['Ensembles', ['ENS', /* 'AIFS_ENS', */ 'GEFS']]];
  const DASH = '5 3', LATEST_DASH = '0.5 3.5', AVG_DASH = '7 4';
  const OBS_W = 2.1;            // every observed line, all panels
  const PANELS = [
    { v: 'temp', title: 'Temperature (°F)', h: 200 },
    { v: 'wind', title: 'Wind (kt)', h: 110 },
    { v: 'precip', title: 'Precip since 06Z (in)', h: 90 },
    { v: 'cloud', title: 'Cloud cover (%)', h: 100 },
    { v: 'td', title: 'Dewpoint (°F)', h: 120, opt: true },
    { v: 'rh', title: 'Relative humidity (%)', h: 100, opt: true },
  ];
  const P = Object.fromEntries(PANELS.map(p => [p.v, p]));
  const LINE_VARS = ['temp', 'wind', 'precip', 'td', 'rh'];   // drawn as plain lines (cloud has steps)
  const TOP = 24, HEAD = 22, BOT = 24, AXW = 40;
  const H25 = Array.from({ length: 25 }, (_, j) => j);

  const STORE = 'wxc-timeline';
  const st = { on: new Set(ORDER), avg: true, obs: true, latest: true, band: true, hum: true };
  try {
    const s = JSON.parse(localStorage.getItem(STORE) || 'null');
    if (s) {
      if (Array.isArray(s.on)) {
        // models added since the viewer's choice was saved start switched on (IFS_HRES predates "known")
        const known = new Set(Array.isArray(s.known) ? s.known : ORDER.filter(n => n !== 'IFS_HRES'));
        st.on = new Set([...s.on, ...ORDER.filter(n => !known.has(n))]);
      }
      for (const k of ['avg', 'obs', 'latest', 'band']) if (typeof s[k] === 'boolean') st[k] = s[k];
      if (typeof s.hum2 === 'boolean') st.hum = s.hum2;   // not 'hum': before they were on by default, every save wrote hum: false
    }
  } catch (e) {}
  const save = () => {
    try { localStorage.setItem(STORE, JSON.stringify({ on: [...st.on], known: ORDER, avg: st.avg, obs: st.obs, latest: st.latest, band: st.band, hum2: st.hum })); }
    catch (e) {}
  };

  // the panels shown (the humidity ones unless switched off), stacked top to bottom
  let VIS = [], H = 0;
  function stack() {
    VIS = PANELS.filter(p => !p.opt || st.hum);
    let yy = TOP;
    for (const p of VIS) { yy += HEAD; p.y0 = yy; yy += p.h; }
    H = yy + BOT;
  }
  stack();
  const shown = v => VIS.includes(P[v]);

  let T = null, ND = 0, DW = 320, W = 0, NOW_H = 0, TODAY_K = 0, present = [], HI = [], AV = [];
  const SC = {};
  let curH = null, pinned = null, touched = false;
  const LENS = 250, ZOOM = 2;     // lens diameter (px) and magnification
  let zoomOn = false;

  /* ---------- helpers ---------- */
  const pad = n => String(n).padStart(2, '0');
  const label = n => n.replace('_', ' ');
  const f0 = v => v == null ? '—' : String(Math.round(v));
  const f2 = v => v == null ? '—' : Number(v).toFixed(2);
  const hourLabel = h => `${pad(((Math.round(h) % 24) + 30) % 24)}Z`;       // hours since day-0 06Z
  const run = iso => { const m = /^\d{4}-(\d{2})-(\d{2})T(\d{2})/.exec(iso || ''); return m ? `${m[3]}Z ${+m[1]}/${+m[2]}` : '—'; };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const finite = a => (a || []).filter(x => x != null && isFinite(x));
  const maxOf = a => { const f = finite(a); return f.length ? Math.max(...f) : null; };
  const minOf = a => { const f = finite(a); return f.length ? Math.min(...f) : null; };
  const lastOf = a => { const f = finite(a); return f.length ? f[f.length - 1] : null; };
  const mean = a => { const f = finite(a); return f.length ? f.reduce((s, x) => s + x, 0) / f.length : null; };
  const dayOf = h => Math.max(0, Math.min(ND - 1, Math.floor(h / 24)));
  const X = h => h / 24 * DW;
  const Y = (p, v) => { const s = SC[p.v], c = Math.max(s.lo, Math.min(s.hi, v)); return p.y0 + p.h * (1 - (c - s.lo) / (s.hi - s.lo)); };

  function lerp(hs, vs, h) {
    if (!hs || !vs || !hs.length || h < hs[0] - 1e-6 || h > hs[hs.length - 1] + 1e-6) return null;
    for (let i = 0; i < hs.length - 1; i++) {
      if (h <= hs[i + 1] + 1e-6) {
        const a = vs[i], b = vs[i + 1];
        if (a == null || b == null) return h - hs[i] < 1e-6 ? a : (hs[i + 1] - h < 1e-6 ? b : null);
        return a + (h - hs[i]) / (hs[i + 1] - hs[i]) * (b - a);
      }
    }
    return vs[vs.length - 1];
  }
  function nearest(hs, vs, h) {        // categorical steps (MOS cloud categories)
    if (!hs || !hs.length || h < hs[0] - 1.5 || h > hs[hs.length - 1] + 1.5) return null;
    let best = 0;
    for (let i = 1; i < hs.length; i++) if (Math.abs(hs[i] - h) < Math.abs(hs[best] - h)) best = i;
    return vs[best];
  }
  function pct(a, q) {
    const s = finite(a).sort((x, y) => x - y);
    if (!s.length) return null;
    const i = (s.length - 1) * q, lo = Math.floor(i), hi = Math.ceil(i);
    return s[lo] + (s[hi] - s[lo]) * (i - lo);
  }

  /* ---------- humidity ---------- */
  // RH (%) from temperature and dewpoint (°F), Magnus formula over water
  const es = f => { const c = (f - 32) / 1.8; return Math.exp(17.625 * c / (243.04 + c)); };
  const rhOf = (t, td) => t == null || td == null ? null : Math.min(100, 100 * es(Math.min(td, t)) / es(t));

  // RH of every model run and report with a dewpoint (unless the run brings its own)
  function addRh() {
    for (const d of T.days) {
      for (const g of [d.models, d.latest || {}]) {
        for (const m of Object.values(g)) if (m.td && m.temp && !m.rh) m.rh = m.temp.map((t, i) => rhOf(t, m.td[i]));
      }
      const r = d.obs && d.obs.reports;
      if (r && r.td) r.rh = r.temp.map((t, i) => rhOf(t, r.td[i]));
    }
  }

  /* ---------- data ---------- */
  function hourly(m) {
    const out = {};
    for (const v of LINE_VARS) out[v] = m[v] && m.h && m.h.length ? H25.map(j => lerp(m.h, m[v], j)) : null;
    const c = m.cloud;
    out.cloud = c ? H25.map(j => c.step ? nearest(c.h, c.pct, j) : lerp(c.h, c.pct, j)) : null;
    return out;
  }

  function prep(data) {
    T = data;
    ND = T.days.length;
    addRh();
    const d0 = T.days[0].date;
    const t0 = Date.UTC(+d0.slice(0, 4), +d0.slice(5, 7) - 1, +d0.slice(8, 10), 6);
    NOW_H = (Date.now() - t0) / 36e5;
    TODAY_K = Math.floor(NOW_H / 24);          // the WxChallenge day (06Z-06Z) the clock is in
    present = ORDER.filter(n => T.days.some(d => d.models[n] || (d.latest || {})[n]));
    HI = T.days.map(d => Object.fromEntries(Object.entries(d.models).map(([n, m]) => [n, hourly(m)])));
    // fixed ranges over the whole period (robust: a bad report can't flatten a panel)
    const vals = { temp: [], wind: [], precip: [] };
    for (const d of T.days) {
      for (const g of [d.models, d.latest || {}]) {
        for (const m of Object.values(g)) {
          for (const v of ['temp', 'wind', 'precip']) vals[v].push(...finite(m[v]));
          vals.temp.push(...finite(m.p10), ...finite(m.p90));
        }
      }
      const r = d.obs && d.obs.reports;
      if (r) { vals.temp.push(...finite(r.temp)); vals.wind.push(...finite(r.wind), ...finite(r.gust)); vals.precip.push(...finite(r.precip)); }
    }
    let lo = pct(vals.temp, 0.005), hi = pct(vals.temp, 0.995);
    if (lo == null) { lo = 40; hi = 70; }
    const tstep = hi - lo > 40 ? 10 : 5;
    lo = Math.floor((lo - 2) / tstep) * tstep;
    hi = Math.max(Math.ceil((hi + 2) / tstep) * tstep, lo + 3 * tstep);
    SC.temp = { lo, hi, step: tstep };
    const wmax = Math.max(10, Math.ceil((pct(vals.wind, 0.995) || 0) / 5) * 5);
    SC.wind = { lo: 0, hi: wmax, step: wmax > 30 ? 10 : 5 };
    const pmax = Math.max(0.1, pct(vals.precip, 0.995) || 0);
    const pstep = [0.05, 0.1, 0.25, 0.5, 1, 2, 5].find(s => pmax / s <= 4) || 10;
    SC.precip = { lo: 0, hi: Math.ceil(pmax / pstep - 1e-9) * pstep, step: pstep, dec: pstep < 0.1 || pstep === 0.25 ? 2 : pstep < 1 ? 1 : 0 };
    SC.cloud = { lo: 0, hi: 100, step: 25 };
    // dewpoint: its own range (it varies less than temperature, so finer ticks)
    const tds = [];
    for (const d of T.days) {
      for (const g of [d.models, d.latest || {}]) for (const m of Object.values(g)) tds.push(...finite(m.td));
      if (d.obs && d.obs.reports) tds.push(...finite(d.obs.reports.td));
    }
    let dlo = pct(tds, 0.005), dhi = pct(tds, 0.995);
    if (dlo == null) { dlo = 30; dhi = 60; }
    const dstep = dhi - dlo > 30 ? 10 : 5;
    dlo = Math.floor((dlo - 2) / dstep) * dstep;
    dhi = Math.max(Math.ceil((dhi + 2) / dstep) * dstep, dlo + 3 * dstep);
    SC.td = { lo: dlo, hi: dhi, step: dstep };
    SC.rh = { lo: 0, hi: 100, step: 25 };
  }

  // hourly mean of the models switched on (not the consensus); an hour needs 3 models
  // (or all of them when fewer are on)
  function average() {
    AV = HI.map(day => {
      const out = {};
      for (const p of PANELS) {
        const ns = Object.keys(day).filter(n => st.on.has(n) && day[n][p.v]);
        const need = Math.min(3, ns.length);
        const vals = H25.map(j => {
          let s = 0, c = 0;
          for (const n of ns) { const x = day[n][p.v][j]; if (x != null) { s += x; c++; } }
          return c && c >= need ? s / c : null;
        });
        out[p.v] = { vals, n: ns.length };
      }
      return out;
    });
  }

  /* ---------- drawing ---------- */
  function path(hs, vs, p, off, gap) {
    let s = '', pen = false, last = null;
    for (let i = 0; i < hs.length; i++) {
      const v = vs[i];
      if (v == null || !isFinite(v)) { pen = false; continue; }
      const h = hs[i] + off;
      if (gap && last != null && h - last > gap) pen = false;
      s += (pen ? 'L' : 'M') + X(h).toFixed(1) + ' ' + Y(p, v).toFixed(1);
      pen = true; last = h;
    }
    return s;
  }
  function bandPolys(hs, lo, hi, p, off, fill) {   // shaded lo..hi area, split where a value is missing
    const out = [];
    let seg = [];
    const flush = () => {
      if (seg.length > 1) {
        const up = seg.map(i => `${X(hs[i] + off).toFixed(1)},${Y(p, hi[i]).toFixed(1)}`);
        const dn = seg.map(i => `${X(hs[i] + off).toFixed(1)},${Y(p, lo[i]).toFixed(1)}`).reverse();
        out.push(`<polygon points="${up.concat(dn).join(' ')}" fill="${fill}" fill-opacity="0.13"/>`);
      }
      seg = [];
    };
    for (let i = 0; i < hs.length; i++) {
      if (lo[i] == null || hi[i] == null || !isFinite(lo[i]) || !isFinite(hi[i])) flush();
      else seg.push(i);
    }
    flush();
    return out;
  }
  function stepPath(hs, vs, p, off) {           // step at the midpoints (MOS cloud categories)
    let s = '', pen = false;
    for (let i = 0; i < hs.length; i++) {
      const v = vs[i];
      if (v == null) { pen = false; continue; }
      const a = i > 0 && vs[i - 1] != null ? (hs[i - 1] + hs[i]) / 2 : hs[i];
      const b = i < hs.length - 1 && vs[i + 1] != null ? (hs[i] + hs[i + 1]) / 2 : hs[i];
      const y = Y(p, v).toFixed(1);
      s += (pen ? 'L' : 'M') + X(a + off).toFixed(1) + ' ' + y + 'L' + X(b + off).toFixed(1) + ' ' + y;
      pen = true;
    }
    return s;
  }
  function runningPath(hs, vs, p, off) {        // observed running total: steps up at each report
    let s = '', prev = null;
    for (let i = 0; i < hs.length; i++) {
      const v = vs[i];
      if (v == null) continue;
      const x = X(hs[i] + off).toFixed(1);
      s += prev == null ? `M${X(off).toFixed(1)} ${Y(p, 0).toFixed(1)}L${x} ${Y(p, 0).toFixed(1)}` : `L${x} ${Y(p, prev).toFixed(1)}`;
      s += `L${x} ${Y(p, v).toFixed(1)}`;
      prev = v;
    }
    return s;
  }
  const ln = (d, c, w, dash, op) => d ? `<path d="${d}" fill="none" stroke="${c}" stroke-width="${w}" ` +
    `stroke-linejoin="round" stroke-linecap="round"${dash ? ` stroke-dasharray="${dash}"` : ''}${op != null ? ` stroke-opacity="${op}"` : ''}/>` : '';
  const dot = (x, y, c) => `<circle cx="${x}" cy="${y.toFixed(1)}" r="3.4" fill="${c}" stroke="var(--bg)" stroke-width="1.5"/>`;
  function sw(kind, dash) {
    const line = (c, w, d) => `<svg width="20" height="10" aria-hidden="true" style="flex:none"><line x1="2" x2="18" y1="5" y2="5" ` +
      `stroke="${c}" stroke-width="${w}" stroke-linecap="round"${d ? ` stroke-dasharray="${d}"` : ''}/></svg>`;
    if (kind === 'AVG') return line('var(--ink-2)', 2.6, '5 3');
    if (kind === 'OBS') return line('var(--ink)', 2.8);
    if (kind === 'HUM') return `<svg width="20" height="12" aria-hidden="true" style="flex:none"><rect x="2" y="1" width="16" height="4" rx="1" ` +
      `fill="none" stroke="var(--ink-2)"/><rect x="2" y="7" width="16" height="4" rx="1" fill="var(--ink-2)" fill-opacity="0.45" stroke="var(--ink-2)"/></svg>`;
    if (kind === 'BAND') return `<svg width="20" height="10" aria-hidden="true" style="flex:none"><rect x="1" y="1" width="18" height="8" rx="2" fill="var(--ink-2)" fill-opacity="0.3"/></svg>`;
    return line(COL[kind] || 'var(--ink-3)', dash === LATEST_DASH ? 3 : 2.5, dash || (DASHED.has(kind) ? '4 3' : ''));
  }

  function dayLabel(k) {
    const d = T.days[k].date;
    const s = new Date(d + 'T12:00Z').toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', timeZone: 'UTC' });
    if (k === TODAY_K) return `Today · ${s}`;
    if (k === TODAY_K + 1) return `Tomorrow · ${s} · forecast`;
    if (k > TODAY_K) return `${s} · forecast`;
    return T.days[k].verif && T.days[k].verif.hindcast ? `${s} · hindcast` : s;
  }

  function axis() {
    axisEl.setAttribute('width', AXW);
    axisEl.setAttribute('height', H);
    let s = '';
    for (const p of VIS) {
      const c = SC[p.v];
      for (let v = c.lo; v <= c.hi + 1e-9; v += c.step) {
        const t = p.v === 'precip' ? v.toFixed(c.dec) : Math.round(v);
        s += `<text x="${AXW - 5}" y="${(Y(p, v) + 4).toFixed(1)}" font-size="11" text-anchor="end" fill="var(--ink-3)">${t}</text>`;
      }
    }
    axisEl.innerHTML = s;
  }

  function titles() {
    wrap.querySelectorAll('.tl-ptitle').forEach(e => e.remove());
    for (const p of VIS) {
      const e = document.createElement('div');
      e.className = 'tl-ptitle';
      e.textContent = p.title;
      e.style.left = (AXW + 4) + 'px';
      e.style.top = (p.y0 - HEAD + 3) + 'px';
      wrap.appendChild(e);
    }
  }

  function render() {
    W = Math.round(DW * ND);
    average();
    const o = [];
    const bottom = H - BOT;
    // the part of the timeline still to come
    const nowIn = NOW_H > 0 && NOW_H < 24 * ND, nx = X(Math.max(0, Math.min(NOW_H, 24 * ND)));
    if (NOW_H < 24 * ND) o.push(`<rect x="${nx.toFixed(1)}" y="${TOP}" width="${(W - nx).toFixed(1)}" height="${bottom - TOP}" fill="var(--ink)" fill-opacity="0.035"/>`);
    for (const p of VIS) {
      const c = SC[p.v];
      for (let v = c.lo; v <= c.hi + 1e-9; v += c.step) {
        const y = Y(p, v).toFixed(1);
        o.push(`<line x1="0" x2="${W}" y1="${y}" y2="${y}" stroke="var(--line)"/>`);
      }
    }
    // day boundaries (06Z), day names, hour ticks
    for (let k = 0; k <= ND; k++) o.push(`<line x1="${k * DW}" x2="${k * DW}" y1="2" y2="${bottom}" stroke="var(--ink-3)" stroke-width="1"/>`);
    // days before the city's first forecast day: tinted like the scoreboard's hindcast columns
    T.days.forEach((d, k) => {
      const hind = d.verif && d.verif.hindcast;
      if (hind) o.push(`<rect x="${k * DW + 1}" y="1" width="${DW - 2}" height="${TOP - 3}" rx="3" fill="var(--hind)"/>`);
      o.push(`<text x="${k * DW + 6}" y="15" font-size="12" font-weight="600" fill="${hind ? 'var(--hind-ink)' : 'var(--ink-2)'}">${esc(dayLabel(k))}</text>`);
    });
    const every = DW >= 260 ? 6 : 12;
    for (let h = 0; h <= 24 * ND; h += every) {
      const x = Math.min(W - 13, Math.max(13, X(h)));
      o.push(`<text x="${x.toFixed(1)}" y="${H - 7}" font-size="11" text-anchor="middle" fill="var(--ink-3)">${hourLabel(h)}</text>`);
    }

    const bands = [], lines = [], latest = [], avg = [];
    T.days.forEach((d, k) => {
      const off = 24 * k;
      for (const n of ORDER) {
        const m = d.models[n];
        if (!m || !st.on.has(n)) continue;
        const dash = DASHED.has(n) ? DASH : '';
        if (st.band && m.p10 && m.p90 && !m.p10.includes(null) && !m.p90.includes(null)) {
          const up = m.h.map((h, i) => `${X(h + off).toFixed(1)},${Y(P.temp, m.p90[i]).toFixed(1)}`);
          const dn = m.h.map((h, i) => `${X(h + off).toFixed(1)},${Y(P.temp, m.p10[i]).toFixed(1)}`).reverse();
          bands.push(`<polygon points="${up.concat(dn).join(' ')}" fill="${COL[n]}" fill-opacity="0.13"/>`);
        }
        const c = m.cloud;
        if (st.band && c && c.sd) {          // NBM sky cover +/- its standard deviation (SSD), clipped to 0-100
          const lo = c.pct.map((v, i) => c.sd[i] == null ? null : Math.max(0, v - c.sd[i]));
          const hi = c.pct.map((v, i) => c.sd[i] == null ? null : Math.min(100, v + c.sd[i]));
          bands.push(...bandPolys(c.h, lo, hi, P.cloud, off, COL[n]));
        }
        for (const v of LINE_VARS) if (m[v] && shown(v)) lines.push(ln(path(m.h, m[v], P[v], off), COL[n], 1.6, dash, 0.9));
        if (m.cloud) lines.push(ln((m.cloud.step ? stepPath : path)(m.cloud.h, m.cloud.pct, P.cloud, off), COL[n], 1.5, dash, 0.9));
      }
      if (st.latest) {
        for (const n of ORDER) {
          const m = (d.latest || {})[n];
          if (!m || !st.on.has(n)) continue;
          for (const v of LINE_VARS) if (m[v] && shown(v)) latest.push(ln(path(m.h, m[v], P[v], off), COL[n], 2, LATEST_DASH));
          if (m.cloud) latest.push(ln((m.cloud.step ? stepPath : path)(m.cloud.h, m.cloud.pct, P.cloud, off), COL[n], 2, LATEST_DASH));
        }
      }
      if (st.avg) for (const p of VIS) avg.push(ln(path(H25, AV[k][p.v].vals, p, off), 'var(--ink-2)', 2.6, AVG_DASH));
    });
    o.push(...bands, ...lines, ...latest, ...avg);

    if (st.obs) {
      // temperature and wind run on across days (broken where reports are missing for 3 h);
      // the precip total restarts at each 06Z, like the scoring
      const R = [];
      T.days.forEach((d, k) => {
        const r = d.obs && d.obs.reports;
        if (r) r.h.forEach((h, i) => R.push({ h: 24 * k + h, t: r.temp[i], w: r.wind[i], g: r.gust[i] }));
      });
      const t = R.filter(r => r.t != null), w = R.filter(r => r.w != null);
      o.push(ln(path(t.map(r => r.h), t.map(r => r.t), P.temp, 0, 3), 'var(--ink)', OBS_W));
      o.push(ln(path(w.map(r => r.h), w.map(r => r.w), P.wind, 0, 3), 'var(--ink)', OBS_W));
      for (const r of R) {
        if (r.g == null) continue;
        const x = X(r.h), y = Y(P.wind, r.g);
        o.push(`<path d="M${(x - 2.4).toFixed(1)} ${(y - 2.4).toFixed(1)}l4.8 4.8m0 -4.8l-4.8 4.8" stroke="var(--ink)" stroke-width="1.3"/>`);
      }
      T.days.forEach((d, k) => {
        const ob = d.obs || {}, r = ob.reports;
        if (r) o.push(ln(runningPath(r.h, r.precip, P.precip, 24 * k), 'var(--ink)', OBS_W));
        if (ob.goes) o.push(ln(path(ob.goes.h, ob.goes.pct, P.cloud, 24 * k, 2), 'var(--ink)', OBS_W));
        if (ob.sky) {
          ob.sky.h.forEach((h, i) => {
            const v = ob.sky.pct[i];
            if (v == null) return;
            const clear = ob.sky.clear && ob.sky.clear[i];
            o.push(`<circle cx="${X(24 * k + h).toFixed(1)}" cy="${Y(P.cloud, v).toFixed(1)}" r="2.6" ` +
                   (clear ? 'fill="var(--bg)" stroke="var(--ink)" stroke-width="1.2"/>' : 'fill="var(--ink)"/>'));
          });
        }
      });
      // dewpoint and RH: every report, run on across days like temperature
      if (st.hum) {
        const R = [];
        T.days.forEach((d, k) => {
          const u = d.obs && d.obs.reports;
          if (u && u.td) u.h.forEach((h, i) => R.push({ h: 24 * k + h, td: u.td[i], rh: u.rh[i] }));
        });
        for (const v of ['td', 'rh']) {
          const s = R.filter(r => r[v] != null);
          o.push(ln(path(s.map(r => r.h), s.map(r => r[v]), P[v], 0, 3), 'var(--ink)', OBS_W));
        }
      }
    }
    if (nowIn) {
      o.push(`<line x1="${nx.toFixed(1)}" x2="${nx.toFixed(1)}" y1="${TOP}" y2="${bottom}" stroke="var(--ink-2)" stroke-dasharray="2 3"/>`);
      o.push(`<text x="${(nx + 4).toFixed(1)}" y="${TOP + 14}" font-size="11" fill="var(--ink-2)">now</text>`);
    }
    o.push('<g id="tl-xh"></g>');
    chart.setAttribute('width', W);
    chart.setAttribute('height', H);
    chart.setAttribute('viewBox', `0 0 ${W} ${H}`);
    chart.innerHTML = `<g id="tl-root">${o.join('')}</g>`;
    axis();
    hover();
  }

  /* ---------- hover: crosshair and day card ---------- */
  function obsAt(k, j) {
    const ob = T.days[k].obs || {}, r = ob.reports, out = {};
    const near = (hs, tol) => {
      let best = -1;
      (hs || []).forEach((h, i) => { if (Math.abs(h - j) <= tol && (best < 0 || Math.abs(h - j) < Math.abs(hs[best] - j))) best = i; });
      return best;
    };
    if (r) {
      const i = near(r.h, 0.75);
      if (i >= 0) { out.t = r.temp[i]; out.w = r.wind[i]; if (r.td) { out.td = r.td[i]; out.rh = r.rh[i]; } }
    }
    if (ob.sky) { const i = near(ob.sky.h, 0.6); if (i >= 0) out.c = ob.sky.pct[i]; }
    return out;
  }
  const at = (t, w, c) => {
    const parts = [t == null ? null : Math.round(t) + '°', w == null ? null : Math.round(w) + ' kt',
                   c == null ? null : Math.round(c) + '%'].filter(Boolean);
    return `<td>${parts.length ? parts.join(', ') : '—'}</td>`;
  };
  // dewpoint and RH at the hovered hour (a column only while the humidity panels are on)
  const atHum = (td, rh) => st.hum ? `<td>${td == null ? '—' : Math.round(td) + '°'} / ${rh == null ? '—' : Math.round(rh) + '%'}</td>` : '';
  function er(e, dec) {
    if (e == null) return '';
    if (Math.abs(e) < 0.5 * Math.pow(10, -dec)) return ' <span class="mu">0</span>';
    return ` <span class="${e > 0 ? 'up' : 'dn'}">${e > 0 ? '+' : '−'}${Math.abs(e).toFixed(dec)}</span>`;
  }
  // mean of hourly values over a cloud window [first, last] (hours since 06Z), if at least
  // half its hours have a value (as the scoreboard's cloud numbers)
  function winMean(vals, w) {
    if (!vals || !w) return null;
    const got = [];
    for (let i = Math.round(w[0]); i <= Math.round(w[1]); i++) if (vals[i] != null) got.push(vals[i]);
    return got.length && got.length >= 0.5 * (w[1] - w[0] + 1) ? mean(got) : null;
  }
  // observed sky cover over a window: per hour the ASOS report nearest the top of the hour
  // (within 35 min), over the hours already past
  function obsWin(k, w) {
    const sky = (T.days[k].obs || {}).sky;
    if (!sky || !w) return null;
    const got = [], last = Math.min(Math.round(w[1]), Math.floor(NOW_H - 24 * k));
    for (let i = Math.round(w[0]); i <= last; i++) {
      let best = -1;
      sky.h.forEach((h, n) => { if (Math.abs(h - i) <= 35 / 60 && (best < 0 || Math.abs(h - i) < Math.abs(sky.h[best] - i))) best = n; });
      if (best >= 0 && sky.pct[best] != null) got.push(sky.pct[best]);
    }
    const hours = last - Math.round(w[0]) + 1;
    return hours > 0 && got.length >= 0.5 * hours ? mean(got) : null;
  }

  function cardHtml(k, h) {
    const d = T.days[k], j = h == null ? null : h - 24 * k, v = d.verif, vm = (v && v.models) || {};
    const win = d.cloud_win || {}, cs = d.cloud_scores, csm = (cs && cs.models) || {};
    const hasCloud = !!(d.cloud_win || cs);
    // cloud cover [night, day, night error, day error]: the scoreboard's numbers on verified
    // days, else the mean of the hourly values over the windows (no error until verified)
    const ocl = cs ? cs.obs : [obsWin(k, win.night), obsWin(k, win.day)];
    const cl = (n, vals) => csm[n] || [winMean(vals, win.night), winMean(vals, win.day), null, null];
    const cc = c => hasCloud ? `<td>${f0(c[0])}${er(c[2], 0)}</td><td>${f0(c[1])}${er(c[3], 0)}</td>` : '';
    const cols = (hasCloud ? '<th title="Mean cloud cover (%) from 06Z to sunrise">Night cloud</th>' +
                             '<th title="Mean cloud cover (%) from sunrise to sunset">Day cloud</th>' : '') +
                 (j == null ? '' : `<th>At ${hourLabel(h)}</th>` + (st.hum ? '<th title="Dewpoint / relative humidity">Td / RH</th>' : ''));
    const notes = [];
    if (d.hindcast) notes.push('These runs were rebuilt afterwards (hindcast) from what was out at 23Z the day before.' +
      (['ENS', 'AIFS_ENS', 'GEFS'].some(n => d.models[n]) ? '' : ' Ensembles can\'t be rebuilt (only their latest run is served), so they are missing.'));
    const rows = [];
    const oa = j == null ? null : obsAt(k, j), oat = j == null ? '' : at(oa.t, oa.w, oa.c) + atHum(oa.td, oa.rh);
    if (v) {
      const o = v.obs;
      rows.push(`<tr class="obs"><td>Observed</td><td>official</td><td>${f0(o[0])}</td><td>${f0(o[1])}</td><td>${f0(o[2])}</td>` +
                `<td>${f2(o[3])}</td>${cc(ocl.concat([null, null]))}${oat}</tr>`);
      notes.push('Errors are forecast minus observed, as on the scoreboard below.');
      if (v.pending && v.pending.length) notes.push(`Not final yet: ${v.pending.join(', ')}.`);
    } else if (d.so_far) {
      const o = d.so_far;
      rows.push(`<tr class="obs"><td>Observed</td><td>so far</td><td>${f0(o.high)}</td><td>${f0(o.low)}</td><td>${f0(o.wind)}</td>` +
                `<td>${f2(o.precip)}</td>${cc(ocl.concat([null, null]))}${oat}</tr>`);
      notes.push(`Observed so far through ${o.through ? o.through.slice(11, 16) + 'Z' : 'now'}.` +
                 (d.latest ? ' Dotted rows are the newest runs.' : ''));
    } else if (k > TODAY_K || (k === TODAY_K && !d.obs)) {
      const deadline = Date.UTC(+d.date.slice(0, 4), +d.date.slice(5, 7) - 1, +d.date.slice(8, 10));
      notes.push(Date.now() < deadline ? 'Forecast only. These runs keep updating until the 00Z deadline.'
                                       : 'Forecast only: the runs that were out at the 00Z deadline.');
    } else {
      notes.push('Official observations not in yet.');
    }
    if (hasCloud) notes.push('Night and day cloud are the mean cover from 06Z to sunrise (drives the low) and from sunrise ' +
                             'to sunset (drives the high); observed by ASOS, not scored.');
    const ns = ORDER.filter(n => st.on.has(n) && d.models[n] && d.models[n].h && d.models[n].h.length);
    const nums = {}, clouds = {};
    for (const n of ns) {
      const m = d.models[n], s = vm[n], hv = HI[k][n];
      const x = s ? s.fc : [m.tmax, m.tmin, maxOf(m.wind), lastOf(m.precip)];
      nums[n] = x;
      clouds[n] = cl(n, hv.cloud);
      rows.push(`<tr><td><span class="tl-m">${sw(n)} ${label(n)}</span></td><td>${run(m.init)}</td>` +
                `<td>${f0(x[0])}${s ? er(s.err[0], 0) : ''}</td><td>${f0(x[1])}${s ? er(s.err[1], 0) : ''}</td>` +
                `<td>${f0(x[2])}${s ? er(s.err[2], 0) : ''}</td><td>${f2(x[3])}${s ? er(s.err[3], 2) : ''}</td>` +
                cc(clouds[n]) + (j == null ? '' : at(hv.temp && hv.temp[j], hv.wind && hv.wind[j], hv.cloud && hv.cloud[j]) +
                                 atHum(hv.td && hv.td[j], hv.rh && hv.rh[j])) + '</tr>');
    }
    if (st.latest && d.latest) {
      for (const n of ORDER) {
        const m = d.latest[n];
        if (!m || !st.on.has(n)) continue;
        const hv = hourly(m);
        rows.push(`<tr class="latest"><td><span class="tl-m">${sw(n, LATEST_DASH)} ${label(n)} newest</span></td><td>${run(m.init)}</td>` +
                  `<td>${f0(m.tmax)}</td><td>${f0(m.tmin)}</td><td>${f0(maxOf(m.wind))}</td><td>${f2(lastOf(m.precip))}</td>` +
                  cc([winMean(hv.cloud, win.night), winMean(hv.cloud, win.day), null, null]) +
                  (j == null ? '' : at(hv.temp && hv.temp[j], hv.wind && hv.wind[j], hv.cloud && hv.cloud[j]) +
                                   atHum(hv.td && hv.td[j], hv.rh && hv.rh[j])) + '</tr>');
      }
    }
    if (st.avg && ns.length) {
      const a = AV[k];
      rows.push(`<tr class="avg"><td><span class="tl-m">${sw('AVG')} Average line</span></td><td>${a.temp.n} model${a.temp.n === 1 ? '' : 's'}</td>` +
                `<td>${f0(maxOf(a.temp.vals))}</td><td>${f0(minOf(a.temp.vals))}</td><td>${f0(maxOf(a.wind.vals))}</td>` +
                `<td>${f2(lastOf(a.precip.vals))}</td>` +
                cc([winMean(a.cloud.vals, win.night), winMean(a.cloud.vals, win.day), null, null]) +
                (j == null ? '' : at(a.temp.vals[j], a.wind.vals[j], a.cloud.vals[j]) + atHum(a.td.vals[j], a.rh.vals[j])) + '</tr>');
      rows.push(`<tr class="avg"><td colspan="2">Mean of the model numbers</td>` +
                [0, 1, 2].map(i => `<td>${f0(mean(ns.map(n => nums[n][i])))}</td>`).join('') +
                `<td>${f2(mean(ns.map(n => nums[n][3])))}</td>` +
                cc([mean(ns.map(n => clouds[n][0])), mean(ns.map(n => clouds[n][1])), null, null]) +
                `${j == null ? '' : '<td></td>' + (st.hum ? '<td></td>' : '')}</tr>`);
      notes.push('The average line\'s high runs lower (and its low higher) than the mean of the model highs and lows when the models disagree on timing.');
    }
    if (!ns.length && !(d.latest && st.latest)) notes.push(Object.keys(d.models).length ? 'No models switched on.' : 'No stored runs for this day.');
    const hint = pinned === k ? 'Pinned. Click the chart again to unpin' : 'Hover a day for its numbers; click to pin it';
    return `<div class="tl-head"><b>${esc(dayLabel(k))}</b><span class="small">${hint}</span></div>` +
      `<p class="small">${notes.map(esc).join(' ')}</p>` +
      (rows.length ? `<table><thead><tr><th>Model</th><th>Run</th><th>High</th><th>Low</th><th>Wind</th><th>Precip</th>${cols}</tr></thead>` +
                     `<tbody>${rows.join('')}</tbody></table>` : '');
  }

  function hover() {
    const g = $('tl-xh');
    if (!g || !T) return;
    const k = curH == null ? null : dayOf(curH);
    let s = '';
    if (k != null) {
      const j = curH - 24 * k, x = X(curH).toFixed(1);
      s += `<line x1="${x}" x2="${x}" y1="${TOP}" y2="${H - BOT}" stroke="var(--ink-2)" stroke-width="1"/>`;
      for (const p of VIS) {
        for (const n of ORDER) {
          const hv = HI[k][n] && HI[k][n][p.v];
          if (hv && st.on.has(n) && hv[j] != null) s += dot(x, Y(p, hv[j]), COL[n]);
        }
        const av = AV[k][p.v].vals[j];
        if (st.avg && av != null) s += dot(x, Y(p, av), 'var(--ink-2)');
      }
      s += `<rect x="${(+x - 18).toFixed(1)}" y="${H - BOT + 3}" width="36" height="17" rx="3" fill="var(--ink)"/>` +
           `<text x="${x}" y="${H - 7}" font-size="11" font-weight="600" text-anchor="middle" fill="var(--bg)">${hourLabel(curH)}</text>`;
    }
    g.innerHTML = s;
    const show = pinned != null ? pinned : k != null ? k : Math.max(0, Math.min(ND - 1, TODAY_K));
    card.innerHTML = cardHtml(show, curH != null && k === show ? curH : null);
  }

  const hourAt = ev => {
    const r = chart.getBoundingClientRect();
    return Math.max(0, Math.min(24 * ND, Math.round((ev.clientX - r.left) / DW * 24)));
  };
  /* ---------- magnifier ---------- */
  function lensAt(ev) {
    if (!zoomOn || !lensSvg) return;
    const r = chart.getBoundingClientRect(), wr = wrap.getBoundingClientRect();
    const cx = ev.clientX - r.left, cy = ev.clientY - r.top;          // chart coordinates (1:1 with the viewBox)
    // on a touch screen, hold the lens above the finger so the finger doesn't cover it
    const lift = ev.pointerType === 'touch' ? LENS / 2 + 24 : 0;
    lens.style.left = (ev.clientX - wr.left - LENS / 2 - 2) + 'px';   // 2: the lens border
    lens.style.top = (ev.clientY - wr.top - LENS / 2 - 2 - lift) + 'px';
    lensSvg.firstChild.setAttribute('transform',
      `translate(${(LENS / 2 - ZOOM * cx).toFixed(1)} ${(LENS / 2 - ZOOM * cy).toFixed(1)}) scale(${ZOOM})`);
    lens.hidden = false;
  }
  function setZoom(on) {
    zoomOn = on;
    if (zoomBtn) zoomBtn.setAttribute('aria-pressed', String(on));
    chart.classList.toggle('tl-zooming', on);
    if (!on && lens) lens.hidden = true;
  }
  if (zoomBtn && lens) {
    lensSvg.setAttribute('width', LENS);
    lensSvg.setAttribute('height', LENS);
    lensSvg.innerHTML = '<use href="#tl-root"/>';
    zoomBtn.addEventListener('click', () => setZoom(!zoomOn));
    document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && zoomOn) setZoom(false); });
  }

  chart.addEventListener('pointermove', ev => { curH = hourAt(ev); hover(); lensAt(ev); });
  chart.addEventListener('pointerleave', () => { curH = null; hover(); if (lens) lens.hidden = true; });
  chart.addEventListener('click', ev => {
    curH = hourAt(ev);
    const k = dayOf(curH);
    pinned = pinned === k ? null : k;
    hover();
  });

  /* ---------- controls ---------- */
  function controls() {
    const chip = (attr, on, inner) => `<button type="button" class="tl-btn" ${attr} aria-pressed="${on}">${inner}</button>`;
    let h = PRESETS.map(([name]) => `<button type="button" class="tl-btn" data-preset="${name}">${name}</button>`).join('');
    h += '<span class="tl-sep"></span>';
    h += present.map(n => chip(`data-m="${n}"`, st.on.has(n), sw(n) + label(n))).join('');
    h += '<span class="tl-sep"></span>';
    h += chip('data-t="avg"', st.avg, sw('AVG') + 'Average') + chip('data-t="obs"', st.obs, sw('OBS') + 'Observed') +
         chip('data-t="latest"', st.latest, sw('HRRR', LATEST_DASH) + 'Newest runs (today)') +
         chip('data-t="band" title="Shaded spread: ensemble 10th–90th percentile temperature, NBM cloud cover ± 1 standard deviation"',
              st.band, sw('BAND') + 'Spread bands');
    h += '<span class="tl-sep"></span>';
    h += chip('data-t="hum" title="Show dewpoint and relative humidity panels below the cloud panel"', st.hum,
              sw('HUM') + 'Dewpoint &amp; RH panels');
    ctl.innerHTML = h;
  }
  ctl.addEventListener('click', ev => {
    const b = ev.target.closest('button');
    if (!b || !T) return;
    if (b.dataset.preset) {
      const list = PRESETS.find(p => p[0] === b.dataset.preset)[1];
      st.on = new Set(list === null ? present : list.filter(n => present.includes(n)));
    } else if (b.dataset.m) {
      const n = b.dataset.m;
      if (st.on.has(n)) st.on.delete(n); else st.on.add(n);
    } else if (b.dataset.t) {
      st[b.dataset.t] = !st[b.dataset.t];
      if (b.dataset.t === 'hum') { stack(); titles(); }     // the chart grows or shrinks
    } else return;
    save();
    controls();
    render();
  });
  $('tl-nav').addEventListener('click', ev => {
    const b = ev.target.closest('button');
    if (!b) return;
    touched = true;
    const go = b.dataset.go;
    if (go === 'today') sc.scrollTo({ left: sc.scrollWidth, behavior: 'smooth' });
    else sc.scrollBy({ left: +go * DW, behavior: 'smooth' });
  });
  ['pointerdown', 'wheel', 'touchstart', 'keydown'].forEach(t => sc.addEventListener(t, () => { touched = true; }, { passive: true }));

  // a day's width: three days across on a wide screen, two on a tablet, one on a phone
  function dayWidth() {
    const a = sc.clientWidth || 600;
    return Math.max(240, Math.floor(a >= 880 ? a / 3 : a >= 540 ? a / 2 : a));
  }
  function layout() {
    const dw = dayWidth();
    if (dw === DW && W) return;
    const left = DW ? sc.scrollLeft / DW : 0;
    DW = dw;
    render();
    sc.scrollLeft = touched ? left * DW : sc.scrollWidth;
  }

  (async function () {
    try {
      const res = await fetch('../data/wxchallenge/timeline.json?t=' + Date.now(), { cache: 'no-store' });
      if (!res.ok) throw new Error('Fetch failed: ' + res.status);
      const data = await res.json();
      if (!data.days || !data.days.length) throw new Error('no days');
      prep(data);
      axisEl.style.width = AXW + 'px';
      chart.setAttribute('aria-label', `Forecasts and observations for ${data.station}, ${data.days[0].date} to ` +
        `${data.days[data.days.length - 1].date}: temperature, wind, precipitation, cloud cover, dewpoint and humidity by hour`);
      sec.hidden = false;      // first, so the scroll box has its width
      controls();
      titles();
      DW = 0;
      layout();
      new ResizeObserver(() => layout()).observe(sc);
    } catch (err) {          // keep the links to the static images
      for (const e of [ctl, $('tl-nav'), wrap, card]) e.style.display = 'none';
      const p = document.createElement('p');
      p.className = 'small';
      p.textContent = 'The interactive timeline is not available right now.';
      ctl.before(p);
      sec.hidden = false;
      console.error(err);
    }
  })();
})();
