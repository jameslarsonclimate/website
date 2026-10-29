/* KLXL pilot weather page: conditions now, nearby TAFs, the hour-by-hour timeline (past 24 h
   observed, 7 days forecast) and the daily flight outlook.
   Data: ../data/klxl/pilot.json, written by klxl_pipeline/klxl_pilot.py. Hours (i) count from
   startUtc; h.* are hourly arrays; shade holds night / civil-twilight spans in the same hours. */
(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const CATV = { VFR: 'var(--vfr)', MVFR: 'var(--mvfr)', IFR: 'var(--ifr)', LIFR: 'var(--lifr)' };
  const catBg = c => CATV[c] || 'var(--unk)';
  const PT = { RA: 'var(--fc)', SN: '#7d8fe0', TS: 'var(--temp)', FZ: '#c2185b', '': '#86b6ef' };
  const PTN = { RA: 'Rain', SN: 'Snow', TS: 'Thunderstorms', FZ: 'Freezing precip', '': 'Precip' };
  const SRC = { obs: 'Observed · KLXL METAR', nbh: 'Forecast · NBM hourly', nbs: 'Forecast · NBM 3-hourly',
                none: 'Forecast · no ceiling / visibility guidance this far out', gap: 'No report this hour' };
  const CONF = { high: 'Based on observations + NBM hourly', med: 'Based on NBM 3-hourly guidance',
                 low: 'Low confidence: no ceiling forecast this far out; outlook from cloud cover' };
  const STORE = 'klxl-pilot';

  let D = null, compact = false, zoom = null, hover = -1, pin = -1, selDay = -1;
  const fmtDir = v => (v == null ? 'VRB' : String(v === 0 ? 360 : v).padStart(3, '0') + '°');
  const f0 = v => (v == null ? '—' : String(Math.round(v)));
  const ft = v => (v == null ? 'None' : v.toLocaleString() + ' ft');

  function zoomTable() {
    return compact ? [['day', '24 h', 13], ['3d', '3 days', 5]] : [['day', '24 h', 40], ['3d', '3 days', 16], ['week', '7 days', 6]];
  }
  function curZoom() {
    const t = zoomTable();
    const z = zoom || (compact ? 'day' : '3d');
    return t.some(r => r[0] === z) ? z : t[0][0];
  }
  const pxFor = z => zoomTable().find(r => r[0] === z)[2];

  /* ---------- conditions now ---------- */
  function renderNow() {
    const el = $('now'), n = D.now, h = D.h;
    if (!n) { el.innerHTML = '<h2 style="font-size:20px">Conditions now</h2><p class="muted">No recent KLXL METAR.</p>'; return; }
    const i0 = Math.floor(D.nowIdx), parts = [];
    let cur = n.cat;
    for (let i = i0 + 1; i <= Math.min(D.N - 1, i0 + 12); i++) {
      if (h.cat[i] && h.cat[i] !== cur) { parts.push(`${h.cat[i]} around ${h.lbl[i]}`); cur = h.cat[i]; }
    }
    const trend = parts.length ? 'Next 12 h: ' + parts.slice(0, 3).join(', then ') : `Next 12 h: staying ${n.cat}`;
    const age = Math.round((Date.now() - Date.parse(n.obsUtc)) / 6e4);
    const d0 = D.days[0] || {};
    const tiles = [
      ['Wind', n.wind, ''], ['Visibility', n.vis, ''], ['Ceiling', n.ceil, ''],
      ['Temp / dew', n.temp, n.spread == null ? '' : n.spread <= 2 ? `Spread ${n.spread}°: fog / low cloud risk` : `Spread ${n.spread}°`, n.spread != null && n.spread <= 2],
      ['Altimeter', n.altim + ' inHg', ''], ['Density altitude', n.da, 'Field elev 1,122 ft'],
      ['Favored runway', n.rwy === '—' ? 'Any (calm)' : 'Rwy ' + n.rwy, n.rwy === '—' ? '' : `${n.head} kt headwind, ${n.xw} kt crosswind`],
      ['Daylight', d0.sr ? `${d0.sr} – ${d0.ss}` : '—', d0.curStart ? `${d0.name}: night landings after ${d0.curStart}` : ''],
    ];
    el.innerHTML =
      `<div class="now-head"><div class="catbox" style="background:${catBg(n.cat)}"><b>${esc(n.cat)}</b><span>right now</span></div>` +
      `<div style="display:flex;flex-direction:column;gap:6px;min-width:0;flex:1 1 300px"><h2 style="font-size:20px">Conditions now</h2>` +
      `<span class="muted" style="font-size:13px">METAR at ${esc(n.time)} (${age} min ago) · ${esc(trend)}</span>` +
      `<code class="mono metar">${esc(n.raw)}</code></div></div>` +
      `<div class="tiles">${tiles.map(([k, v, note, warn]) =>
        `<div class="tile"><span class="k">${esc(k)}</span><span class="v">${esc(v)}</span><span class="n${warn ? ' warn' : ''}">${esc(note)}</span></div>`).join('')}</div>`;
  }

  /* ---------- TAFs ---------- */
  function renderTafs() {
    const el = $('tafs');
    const head = el.firstElementChild.outerHTML;
    if (!D.tafs.length) { el.innerHTML = head + '<p class="muted">No TAFs available right now.</p>'; return; }
    el.innerHTML = head + D.tafs.map(f => {
      if (!f.groups.length) return '';
      const base = f.groups.filter(g => g.kind !== 'TEMPO' && !/^PROB/.test(g.kind));
      const a0 = Math.min(...f.groups.map(g => g.a)), b0 = Math.max(...f.groups.map(g => g.b));
      const pct = v => ((v - a0) / (b0 - a0)) * 100;
      const blocks = base.map((g, k) => {
        const end = k + 1 < base.length ? base[k + 1].a : g.b, w = pct(end) - pct(g.a);
        return `<div style="left:${pct(g.a)}%;width:${w}%;background:${catBg(g.cat)}">${w >= 13 ? g.cat : ''}</div>`;
      }).join('');
      const temp = f.groups.filter(g => g.kind === 'TEMPO' || /^PROB/.test(g.kind));
      const tbars = temp.map(g => `<div class="tempo" style="left:${pct(g.a)}%;width:${pct(g.b) - pct(g.a)}%;background:${catBg(g.cat)}"></div>`).join('');
      const tg = temp[0];
      return `<div style="display:flex;flex-direction:column;gap:6px">` +
        `<div style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap"><strong style="font-size:15px">${esc(f.id)}</strong>` +
        `<span class="muted" style="font-size:12.5px">${esc(f.name)} · ${f.nm} nm ${esc(f.dir)} · issued ${esc(f.issued)}</span></div>` +
        `<div class="tafbar" aria-hidden="true">${blocks}${tbars}</div>` +
        `<div class="row3"><span>${esc(f.groups[0].from_)}</span><span>${tg ? esc(`${tg.kind} ${tg.cat} ${tg.from_}–${tg.to}`) : ''}</span>` +
        `<span>${esc(f.groups[f.groups.length - 1].to)}</span></div>` +
        `<pre class="mono tafraw">${esc(f.raw)}</pre></div>`;
    }).join('');
  }

  /* ---------- timeline ---------- */
  const scroller = $('tl-scroll'), svg = $('tl-svg'), gut = $('tl-gutter');
  let G = null;     // geometry of the last render (px, N, panels)

  function renderTimeline() {
    const h = D.h, N = D.N, px = pxFor(curZoom()), W = N * px;
    // hour i is the column [i*px, (i+1)*px] and its time is the column's centre, so every time on
    // the chart (hour labels, day lines, night shading, now) is drawn at (hours + 0.5) * px
    const cx = i => i * px + px / 2, tx = hrs => (hrs + 0.5) * px;
    const spec = compact
      ? [['axis', 36], ['cat', 22], ['ceil', 120], ['vis', 84], ['wind', 116], ['temp', 84], ['precip', 56], ['aloft', 84]]
      : [['axis', 38], ['cat', 26], ['ceil', 138], ['vis', 96], ['wind', 140], ['temp', 104], ['clouds', 76], ['precip', 70], ['fzl', 84], ['aloft', 100]];
    const titles = compact
      ? { cat: 'Category', ceil: 'Ceiling', vis: 'Vis SM', wind: 'Wind kt', temp: 'T / Td °C', precip: 'Precip', aloft: 'Aloft ft' }
      : { cat: 'Category', ceil: 'Ceiling ft AGL', vis: 'Visibility SM', wind: 'Wind kt', temp: 'Temp / dew °C', clouds: 'Cloud cover', precip: 'Precip chance', fzl: 'Freezing lvl MSL', aloft: 'Winds aloft MSL' };
    const gap = compact ? 8 : 10, gw = compact ? 58 : 112;
    const P = {};
    let y = 0;
    spec.forEach(([k, ht]) => { P[k] = { top: y, h: ht }; y += ht + gap; });
    const H = y - gap, fs = compact ? 10 : 12, ts = compact ? 10 : 11;
    const hd = compact ? 17 : 20;     // title band at the top of each panel: no tick labels in it
    G = { px, N, H, W };

    const g = [], o = [];          // gutter svg, chart svg
    spec.forEach(([k], n) => {
      if (titles[k]) {                // the category strip is one row, so its title is centred on it
        const ty = k === 'cat' ? P.cat.top + P.cat.h / 2 + fs * 0.36 : P[k].top + fs + 1;
        g.push(`<text x="6" y="${ty.toFixed(1)}" font-size="${fs}" font-weight="600" fill="var(--ink)">${esc(titles[k])}</text>`);
      }
      if (n > 0) o.push(`<rect x="0" y="${P[k].top - gap / 2}" width="${W}" height="1" fill="var(--line)"/>`);
    });
    const tick = (k, top, text, grid) => {
      if (top - P[k].top >= hd - 1) g.push(`<text x="${gw - 6}" y="${top + 4}" font-size="${ts}" text-anchor="end" fill="var(--ink-3)">${esc(text)}</text>`);
      if (grid) o.push(`<line x1="0" x2="${W}" y1="${top}" y2="${top}" stroke="var(--grid)" stroke-dasharray="4 3"/>`);
    };
    const band = (a, b, fill) => o.unshift(`<rect x="0" y="${a}" width="${W}" height="${Math.max(0, b - a)}" fill="${fill}"/>`);
    const grp = i => (h.src[i] === 'obs' ? 'obs' : h.src[i] === 'nbh' || h.src[i] === 'nbs' ? 'fc' : 'x');
    const grpW = i => (h.src[i] === 'obs' ? 'obs' : 'fc');
    const path = (vals, yf, want, gf, nullAs) => {
      let d = '', pen = false;
      for (let i = 0; i < N; i++) {
        const inG = gf(i) === want || (i + 1 < N && gf(i + 1) === want && gf(i) !== 'x');
        let v = vals[i];
        if (v == null) v = nullAs;
        if (!inG || v == null) { pen = false; continue; }
        d += (pen ? 'L' : 'M') + cx(i).toFixed(1) + ' ' + yf(v).toFixed(1) + ' ';
        pen = true;
      }
      return d;
    };
    const line = (d, stroke, w, dash) => d ? `<path d="${d}" fill="none" stroke="${stroke}" stroke-width="${w}" stroke-linejoin="round"${dash ? ` stroke-dasharray="${dash}"` : ''}/>` : '';
    const arrow = (x, yy, deg, txt) => `<g transform="translate(${(x - 7).toFixed(1)} ${yy.toFixed(1)})"><path d="M7 13 L7 2 M3 6 L7 2 L11 6" transform="rotate(${deg} 7 7)" fill="none" stroke="var(--arrow)" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>` +
      (txt ? `<text x="16" y="11" font-size="10.5" fill="var(--arrow)">${txt}</text>` : '') + '</g>';

    // night / civil twilight shading and the observed past
    const nowX = tx(D.nowIdx);
    const shades = D.shade.map(z => { const a = Math.max(0, tx(z.a)), b = Math.min(W, tx(z.b)); return b <= a ? '' :
      `<rect x="${a.toFixed(1)}" y="${P.cat.top}" width="${(b - a).toFixed(1)}" height="${H - P.cat.top}" fill="${z.k === 'night' ? 'var(--night)' : 'var(--civil)'}"/>`; }).join('');

    // ceiling (log scale; no ceiling drawn at the top)
    const lg = v => Math.log(1 + v / 250), LM = lg(12000);
    const yC = v => P.ceil.top + P.ceil.h - 4 - (P.ceil.h - hd - 6) * lg(Math.min(v, 12000)) / LM;
    band(yC(3000), yC(1000), 'rgba(31,95,209,.09)');
    band(yC(1000), yC(500), 'rgba(209,47,47,.10)');
    band(yC(500), yC(0), 'rgba(162,28,175,.11)');
    [[500, '500'], [1000, '1,000'], [3000, '3,000'], [12000, compact ? 'None' : 'None / 12k+']].forEach(([v, t]) => tick('ceil', yC(v), t, true));

    // visibility
    const yV = v => P.vis.top + P.vis.h - 3 - (P.vis.h - hd - 5) * Math.min(v, 10) / 10;
    band(yV(5), yV(3), 'rgba(31,95,209,.09)');
    band(yV(3), yV(1), 'rgba(209,47,47,.10)');
    band(yV(1), yV(0), 'rgba(162,28,175,.11)');
    [[3, '3'], [5, '5'], [10, '10+']].forEach(([v, t]) => tick('vis', yV(v), t, true));

    // wind, gusts, crosswind
    const gmax = Math.max(...h.wgst.map(v => v || 0), ...h.wspd.map(v => v || 0));
    const wmax = Math.max(25, Math.ceil((gmax + 3) / 5) * 5);
    const yW = v => P.wind.top + P.wind.h - 3 - (P.wind.h - hd - 10) * Math.min(v, wmax) / wmax;
    for (let v = 10; v <= wmax; v += 10) tick('wind', yW(v), String(v), true);
    let gust = '';
    const r = Math.max(2, Math.min(5, px * 0.35));
    h.wgst.forEach((gv, i) => { if (gv) gust += `M${(cx(i) - r).toFixed(1)} ${yW(gv).toFixed(1)} H${(cx(i) + r).toFixed(1)} `; });
    const base = yW(0).toFixed(1);
    let xwArea = `M${cx(0).toFixed(1)} ${base} `;
    h.xwg.forEach((v, i) => { xwArea += `L${cx(i).toFixed(1)} ${yW(v || 0).toFixed(1)} `; });
    xwArea += `L${cx(N - 1).toFixed(1)} ${base} Z`;
    const arrows = [];
    const kA = [1, 2, 3, 6, 12].find(k => k * px >= 24) || 12;
    for (let i = 0; i < N; i += kA) if (h.wdir[i] != null && h.wspd[i]) arrows.push(arrow(cx(i), P.wind.top + 3, h.wdir[i] + 180, ''));

    // temperature / dewpoint, with the small-spread marks
    const tv = h.tc.concat(h.dc).filter(v => v != null);
    const tmin = Math.floor(Math.min(...tv)) - 1, tmax = Math.ceil(Math.max(...tv)) + 1;
    const yT = v => P.temp.top + P.temp.h - 9 - (P.temp.h - hd - 12) * (v - tmin) / (tmax - tmin);
    for (let v = Math.ceil(tmin / 5) * 5; v <= tmax; v += 5) tick('temp', yT(v), String(v), v !== 0);
    if (tmin < 0 && tmax > 0) o.push(`<line x1="0" x2="${W}" y1="${yT(0)}" y2="${yT(0)}" stroke="#86b6ef"/>`);
    let s0 = -1;
    for (let i = 0; i <= N; i++) {
      const on = i < N && h.tc[i] != null && h.dc[i] != null && h.tc[i] - h.dc[i] <= 2;
      if (on && s0 < 0) s0 = i;
      if (!on && s0 >= 0) { o.push(`<rect x="${s0 * px + 1}" y="${P.temp.top + P.temp.h - 6}" width="${Math.max(1, (i - s0) * px - 2)}" height="5" rx="2.5" fill="var(--spread)"/>`); s0 = -1; }
    }

    // cloud cover rows (GFS low / mid / high)
    if (P.clouds) {
      const rowH = (P.clouds.h - hd - 2) / 3;
      [['ch', 0, 'High'], ['cm', 1, 'Mid'], ['cl', 2, 'Low']].forEach(([k, row, lbl]) => {
        const top = P.clouds.top + hd + row * rowH;
        g.push(`<text x="${gw - 6}" y="${(top + (rowH - 2) / 2 + ts * 0.36).toFixed(1)}" font-size="${ts}" text-anchor="end" fill="var(--ink-3)">${lbl}</text>`);
        const q = v => Math.round((v || 0) / 10);
        let s = 0;
        for (let i = 1; i <= N; i++) {
          if (i === N || q(h[k][i]) !== q(h[k][s])) {
            const a = q(h[k][s]) / 10;
            if (a > 0) o.push(`<rect x="${s * px}" y="${top}" width="${(i - s) * px}" height="${rowH - 2}" fill="rgba(var(--cloud),${(a * 0.7).toFixed(2)})"/>`);
            s = i;
          }
        }
      });
    }

    // precip chance bars, coloured by type
    const pad = px > 6 ? 1 : 0;
    h.pop.forEach((v, i) => {
      if (v >= 5) {
        const hh = (P.precip.h - hd - 2) * v / 100;
        o.push(`<rect x="${i * px + pad}" y="${P.precip.top + P.precip.h - hh}" width="${Math.max(1, px - 2 * pad)}" height="${hh}" rx="1.5" fill="${PT[h.pt[i]] || PT['']}"/>`);
      }
    });
    tick('precip', P.precip.top + P.precip.h - (P.precip.h - hd - 2) * 0.5, '50%', true);

    // freezing level
    let fLine = '';
    if (P.fzl) {
      const yF = v => P.fzl.top + P.fzl.h - 4 - (P.fzl.h - hd - 6) * Math.min(v, 14000) / 14000;
      [[4000, '4k'], [8000, '8k'], [12000, '12k']].forEach(([v, t]) => tick('fzl', yF(v), t, true));
      fLine = path(h.fzl, yF, 'all', () => 'all');
    }

    // winds aloft (highest level on top)
    const rowA = (P.aloft.h - hd - 2) / 3;
    const kB = [1, 2, 3, 6, 12].find(k => k * px >= (compact ? 36 : 42)) || 12;
    [['a3', 2], ['a2', 1], ['a1', 0]].forEach(([k, lev], row) => {
      const top = P.aloft.top + hd + row * rowA;
      if (D.levFt[lev]) g.push(`<text x="${gw - 6}" y="${(top + rowA / 2 + ts * 0.36).toFixed(1)}" font-size="${ts}" text-anchor="end" fill="var(--ink-3)">${D.levFt[lev] / 1000}k</text>`);
      for (let i = 0; i < N; i += kB) if (h[k + 'd'][i] != null) arrows.push(arrow(cx(i), top + (rowA - 14) / 2, h[k + 'd'][i] + 180, String(h[k + 's'][i])));
    });

    // flight category strip (hatched grey: no ceiling guidance)
    const key = i => (h.cat[i] || h.src[i]);
    let s = 0;
    for (let i = 1; i <= N; i++) {
      if (i === N || key(i) !== key(s)) {
        const w = (i - s) * px, c = h.cat[s];
        if (c || h.src[s] === 'none') {
          o.push(`<rect x="${s * px}" y="${P.cat.top + 2}" width="${Math.max(0, w - 1)}" height="${P.cat.h - 4}" rx="3" fill="${catBg(c)}"${c ? '' : ' fill-opacity="0.7"'}/>`);
          if (!c) o.push(`<rect x="${s * px}" y="${P.cat.top + 2}" width="${Math.max(0, w - 1)}" height="${P.cat.h - 4}" rx="3" fill="url(#hatch)"/>`);
          const lab = c || (w >= 120 ? 'no ceiling fcst' : '');
          if (w >= (c ? 44 : 120)) o.push(`<text x="${s * px + w / 2}" y="${P.cat.top + P.cat.h / 2 + 4}" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">${lab}</text>`);
        }
        s = i;
      }
    }

    // axis: day lines and names, hour labels
    const lh = t => (parseInt(t, 10) % 12) + (t.endsWith('p') ? 12 : 0);
    const kH = [1, 2, 3, 6, 12].find(k => k * px >= (compact ? 28 : 32)) || 12;
    const dayName = i => { const n = h.t[i].split(',')[0]; return compact ? n.replace(/^(\w+) \w+ /, '$1 ') : n; };
    const days = [];                 // [x, name] of each midnight, for stickyDay()
    h.dayStart.forEach((ds, i) => {
      if (ds) {
        days.push([cx(i), dayName(i)]);
        if (W - cx(i) > (compact ? 50 : 80))      // not one too close to the right edge to fit
          o.push(`<text x="${cx(i) + 5}" y="15" font-size="12" font-weight="700" fill="var(--ink)">${esc(dayName(i))}</text>`);
        o.push(`<rect x="${cx(i)}" y="0" width="1" height="${H}" fill="var(--ink-3)" fill-opacity="0.45"/>`);
      }
      const x = cx(i);
      if (lh(h.lbl[i]) % kH === 0 && x >= 10 && x <= W - 10 && Math.abs(x - nowX) > 34)
        o.push(`<text x="${x}" y="${P.axis.h - 6}" font-size="10.5" text-anchor="middle" fill="var(--ink-3)">${ds ? '12a' : h.lbl[i]}</text>`);
    });

    const lines = [
      `<path d="${xwArea}" fill="var(--xw)" fill-opacity="0.2"/>`,
      line(path(h.xw, yW, 'all', () => 'all'), 'var(--xw)', 1.5),
      gust ? `<path d="${gust}" fill="none" stroke="var(--ink-3)" stroke-width="2" stroke-linecap="round"/>` : '',
      line(path(h.wspd, yW, 'obs', grpW), 'var(--obs)', 2), line(path(h.wspd, yW, 'fc', grpW), 'var(--fc)', 2),
      line(path(h.ceil, yC, 'obs', grp, 12000), 'var(--obs)', 2), line(path(h.ceil, yC, 'fc', grp, 12000), 'var(--fc)', 2),
      line(path(h.vis, yV, 'obs', grp), 'var(--obs)', 2), line(path(h.vis, yV, 'fc', grp), 'var(--fc)', 2),
      line(path(h.tc, yT, 'all', () => 'all'), 'var(--temp)', 2), line(path(h.dc, yT, 'all', () => 'all'), 'var(--dew)', 2),
      line(fLine, 'var(--fzl)', 2),
      `<line x1="0" x2="${W}" y1="${yW(D.xwLimit)}" y2="${yW(D.xwLimit)}" stroke="var(--xw)" stroke-width="2" stroke-dasharray="6 4" opacity="0.8"/>`,
    ].join('');

    svg.setAttribute('width', W);
    svg.setAttribute('height', H);
    svg.innerHTML =
      '<defs><pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">' +
      '<rect width="3" height="7" fill="rgba(255,255,255,.45)"/></pattern></defs>' +
      `<rect x="0" y="0" width="${nowX}" height="${H}" fill="var(--past)"/>` + shades + o.join('') + lines + arrows.join('') +
      `<rect x="${nowX - 1}" y="0" width="2" height="${H}" fill="var(--ink)"/>` +
      `<g><rect x="${nowX - 17}" y="${P.axis.h - 18}" width="34" height="15" rx="4" fill="var(--ink)"/>` +
      `<text x="${nowX}" y="${P.axis.h - 7}" font-size="10" font-weight="700" text-anchor="middle" fill="var(--bg)">NOW</text></g>` +
      `<g id="tl-day"><rect x="0" y="1" height="19" fill="var(--card)"/><text x="5" y="15" font-size="12" font-weight="700" fill="var(--ink)"></text></g>` +
      '<g id="tl-hover"></g>';
    gut.setAttribute('width', gw);
    gut.setAttribute('height', H);
    gut.style.width = gw + 'px';
    gut.innerHTML = g.join('');
    G.days = days;
    G.firstDay = dayName(0);
    stickyDay();
    $('zooms').innerHTML = zoomTable().map(([id, label]) => `<button type="button" data-z="${id}" aria-pressed="${id === curZoom()}">${label}</button>`).join('');
    renderHover();
  }

  // the day at the left edge of the view (its own name has scrolled out of sight)
  function stickyDay() {
    const el = svg.querySelector('#tl-day');
    if (!el || !G) return;
    const left = scroller.scrollLeft, txt = el.querySelector('text'), bg = el.querySelector('rect');
    let name = G.firstDay, next = null;
    for (const [x, n] of G.days) { if (x <= left + 1) name = n; else { next = x; break; } }
    txt.textContent = name;
    el.style.display = '';                           // measurable again
    const w = txt.getComputedTextLength() + 10;
    el.setAttribute('transform', `translate(${left.toFixed(1)} 0)`);
    bg.setAttribute('width', w);
    el.style.display = next != null && next - left < w + 4 ? 'none' : '';   // the next day's name is about to take over
  }
  scroller.addEventListener('scroll', stickyDay, { passive: true });

  function selIndex() {
    const nowI = Math.min(D.N - 1, Math.floor(D.nowIdx));
    return hover >= 0 ? hover : pin >= 0 ? pin : nowI;
  }

  function renderHover() {
    const el = svg.querySelector('#tl-hover');
    if (!el || !G) return;
    const i = selIndex(), px = G.px;
    el.innerHTML = `<rect x="${i * px}" y="0" width="${px}" height="${G.H}" fill="var(--ink)" fill-opacity="0.06"/>` +
      `<rect x="${i * px + px / 2}" y="0" width="1" height="${G.H}" fill="var(--ink)" fill-opacity="0.6"/>`;
    renderReadout(i);
  }

  function renderReadout(i) {
    const h = D.h;
    const lev = n => D.levFt[n] ? D.levFt[n].toLocaleString() + ' ft' : `level ${n + 1}`;
    const nocat = !h.cat[i];
    const items = [
      ['Ceiling', nocat && h.src[i] !== 'obs' ? 'No forecast' : h.ceil[i] == null ? 'None' : h.ceil[i].toLocaleString() + ' ft AGL'],
      ['Visibility', nocat && h.src[i] !== 'obs' ? 'No forecast' : h.vis[i] == null ? '—' : (h.vis[i] >= 10 ? '10+' : h.vis[i]) + ' SM'],
      ['Wind', !h.wspd[i] ? 'Calm' : `${fmtDir(h.wdir[i])} ${h.wspd[i]} kt` + (h.wgst[i] ? ` G${h.wgst[i]}` : '')],
      ['Crosswind', h.rwy[i] === '—' ? 'Calm' : `Rwy ${h.rwy[i]}: ${h.xw[i]} kt` + (h.xwg[i] > h.xw[i] ? `, G${h.xwg[i]}` : '')],
      ['Temp / dew', `${f0(h.tc[i])}° / ${f0(h.dc[i])}°C`],
      ['Density altitude', h.da[i] == null ? '—' : h.da[i].toLocaleString() + ' ft'],
      ['Sky cover', h.sky[i] == null ? '—' : h.sky[i] + '%'],
      ['Cloud L / M / H', `${f0(h.cl[i])} / ${f0(h.cm[i])} / ${f0(h.ch[i])}%`],
      ['Precip', h.pop[i] ? `${PTN[h.pt[i]] || 'Precip'} ${h.pop[i]}%` : 'None'],
      ['Freezing level', h.fzl[i] == null ? '—' : h.fzl[i].toLocaleString() + ' ft MSL'],
      ['Wind ' + lev(0), h.a1d[i] == null ? '—' : `${fmtDir(h.a1d[i])} ${h.a1s[i]} kt`],
      ['Wind ' + lev(1), h.a2d[i] == null ? '—' : `${fmtDir(h.a2d[i])} ${h.a2s[i]} kt`],
      ['Wind ' + lev(2), h.a3d[i] == null ? '—' : `${fmtDir(h.a3d[i])} ${h.a3s[i]} kt, ${f0(h.a3t[i])}°C`],
    ];
    $('readout').innerHTML =
      `<div class="ro-head"><span class="pill" style="background:${catBg(h.cat[i])}">${esc(h.cat[i] || '—')}</span>` +
      `<strong style="font-size:15px">${esc(h.t[i])}</strong><span class="muted" style="font-size:12px">${esc(SRC[h.src[i]] || '')}</span>` +
      `<span style="margin-left:auto;display:flex;gap:6px"><button type="button" class="btn" data-step="-1" aria-label="Previous hour" style="min-width:40px;font-size:16px">‹</button>` +
      `<button type="button" class="btn" data-step="1" aria-label="Next hour" style="min-width:40px;font-size:16px">›</button></span></div>` +
      `<div class="ro-grid">${items.map(([k, v]) => `<div style="display:flex;flex-direction:column;gap:2px;min-width:0"><span class="k">${esc(k)}</span><span class="v">${esc(v)}</span></div>`).join('')}</div>`;
  }

  function scrollToHour(i, smooth) {
    const left = Math.max(0, i * pxFor(curZoom()));
    if (smooth) scroller.scrollTo({ left, behavior: 'smooth' }); else scroller.scrollLeft = left;
  }
  function setZoom(z) {
    const old = pxFor(curZoom()), center = (scroller.scrollLeft + scroller.clientWidth / 2) / old;
    zoom = z;
    try { localStorage.setItem(STORE, JSON.stringify({ zoom })); } catch (e) {}
    renderTimeline();
    scroller.scrollLeft = Math.max(0, center * pxFor(curZoom()) - scroller.clientWidth / 2);
  }
  const hourAt = ev => {
    const rc = svg.getBoundingClientRect();
    return Math.max(0, Math.min(D.N - 1, Math.floor((ev.clientX - rc.left) / G.px)));
  };

  /* ---------- daily outlook ---------- */
  function renderDays() {
    $('outlook-rule').textContent = `Outlook = the longest daylight stretch that is VFR with crosswind at or below ${D.xwLimit} kt, ` +
      `gusts at or below ${D.gustLimit} kt, precip chance under 50% and no thunderstorms. Good: 6 h or more · Fair: 3–5 h · ` +
      `Poor: less than 3 h. The bar is each daylight hour's flight category (hatched grey: no ceiling forecast, so sky cover ` +
      `under ${D.skyOk}% counts as likely VFR).`;
    $('days').innerHTML = D.days.map((d, k) => {
      const bad = 'bad';
      const rows = [
        ['VFR window', d.winH ? `${d.win} (${d.winH} h)` : 'None', d.winH ? '' : bad],
        ['Lowest ceiling', d.ceilKnown ? ft(d.minCeil) : (d.minCeil == null ? 'No forecast' : ft(d.minCeil) + '+')],
        ['Lowest vis', d.minVis == null ? (d.ceilKnown ? '—' : 'No forecast') : (d.minVis >= 10 ? '10+' : d.minVis) + ' SM'],
        ['Wind', d.maxWind + (d.maxGust ? ' G' + d.maxGust : '') + ' kt', d.maxGust > D.gustLimit ? bad : ''],
        ['Max crosswind', `${d.maxXw}${d.maxXwg > d.maxXw ? ' G' + d.maxXwg : ''} kt · ${d.xwRwy === '—' ? 'calm' : 'Rwy ' + d.xwRwy}`, d.maxXw > D.xwLimit ? bad : ''],
        ['Precip', d.pop >= 10 ? `${PTN[d.ptype] || 'Precip'} ${d.pop}%` : 'None'],
        ['Freezing lvl', ft(d.fzlMin)],
        ['Wind ' + (D.levFt[0] ? D.levFt[0] / 1000 + 'k ft' : 'aloft'), d.aloft === '—' ? '—' : d.aloft + ' kt'],
        ['Night landings', `${d.curStart} – ${d.curEnd}`],
      ];
      const strip = d.strip.map((c, n) => `<span class="${c ? '' : 'hatch'}" style="background-color:${catBg(c)}${c ? '' : ';opacity:.7'}"></span>`).join('');
      return `<button type="button" class="day" data-day="${k}" aria-pressed="${k === selDay}">` +
        `<span class="top1"><span style="font-size:18px;font-weight:700">${esc(d.name)}</span><span class="small">${esc(d.date)}</span>` +
        `<span class="outlook o-${d.outlook}">${esc(d.outlook)}</span></span>` +
        `<span style="display:flex;flex-direction:column;gap:2px;min-height:34px"><span style="font-size:13px;line-height:1.3">${esc(d.why)}</span>` +
        `<span class="small" style="font-size:12px;line-height:1.3">${esc(d.why2)}</span></span>` +
        `<span style="display:flex;flex-direction:column;gap:3px;width:100%"><span class="strip" aria-hidden="true">${strip}</span>` +
        `<span class="row3"><span>Sunrise ${esc(d.sr)}</span><span>Sunset ${esc(d.ss)}</span></span></span>` +
        `<span class="stats">${rows.map(([kk, v, c]) => `<span style="display:flex;flex-direction:column;gap:1px;min-width:0"><span class="k" style="font-size:10.5px">${esc(kk)}</span>` +
          `<span class="v${c ? ' ' + c : ''}">${esc(v)}</span></span>`).join('')}</span>` +
        `<span class="small" style="margin-top:auto;font-size:11px">${esc(CONF[d.conf] || '')}</span></button>`;
    }).join('');
  }

  function legend() {
    $('legend').innerHTML = [
      ['<span class="sw" style="background:var(--obs)"></span>', 'Observed (METAR)'],
      ['<span class="sw" style="background:var(--fc)"></span>', 'Forecast'],
      ['<span class="sw" style="width:14px;height:10px;background:var(--xw);opacity:.35"></span>', 'Crosswind, best runway'],
      ['<span class="sw" style="height:0;border-top:2px dashed var(--xw)"></span>', `Crosswind limit ${D.xwLimit} kt`],
      ['<span class="sw" style="width:10px;height:2px;border-radius:1px;background:var(--ink-3)"></span>', 'Gusts'],
      ['<span class="sw" style="height:2px;background:var(--temp)"></span>', 'Temperature'],
      ['<span class="sw" style="height:2px;background:var(--dew)"></span>', 'Dewpoint'],
      ['<span class="sw" style="width:14px;height:5px;border-radius:3px;background:var(--spread)"></span>', 'Temp-dew spread 2 °C or less'],
      ...(compact ? [] : [['<span class="sw" style="height:2px;background:var(--fzl)"></span>', 'Freezing level']]),
      ['<span style="gap:2px">' + ['RA', 'SN', 'FZ', 'TS'].map(k => `<span class="sw" style="width:6px;height:10px;border-radius:1.5px;background:${PT[k]}"></span>`).join('') + '</span>',
       'Precip: rain, snow, freezing, thunder'],
      ['<span class="sw" style="width:14px;height:10px;background:var(--night);outline:1px solid var(--line)"></span>', 'Night / civil twilight'],
    ].map(([sw, t]) => `<span>${sw}${esc(t)}</span>`).join('');
  }

  function status() {
    const el = $('status');
    const age = (Date.now() - Date.parse(D.generated_at_utc)) / 36e5;
    const msgs = [];
    if (age > 2) msgs.push(`This page was last updated ${Math.round(age)} hours ago, so the conditions and forecast may be out of date.`);
    if (D.notes && D.notes.length) msgs.push('Some data could not be fetched: ' + D.notes.join('; ') + '.');
    el.textContent = msgs.join(' ');
    el.hidden = !msgs.length;
  }

  /* ---------- wiring ---------- */
  $('zooms').addEventListener('click', ev => { const b = ev.target.closest('button[data-z]'); if (b) setZoom(b.dataset.z); });
  $('go-now').addEventListener('click', () => { pin = -1; hover = -1; renderHover(); scrollToHour(D.nowIdx - (compact ? 3 : 8), true); });
  svg.addEventListener('pointermove', ev => { if (ev.pointerType !== 'mouse' || !G) return; const j = hourAt(ev); if (j !== hover) { hover = j; renderHover(); } });
  svg.addEventListener('pointerleave', () => { hover = -1; if (G) renderHover(); });
  svg.addEventListener('click', ev => { if (!G) return; pin = hourAt(ev); hover = -1; renderHover(); });
  $('readout').addEventListener('click', ev => {
    const b = ev.target.closest('button[data-step]');
    if (!b) return;
    const i = Math.max(0, Math.min(D.N - 1, selIndex() + +b.dataset.step));
    pin = i; hover = -1;
    renderHover();
    const px = G.px;
    if (i * px < scroller.scrollLeft || (i + 1) * px > scroller.scrollLeft + scroller.clientWidth) scroller.scrollLeft = i * px - scroller.clientWidth / 2;
  });
  $('days').addEventListener('click', ev => {
    const b = ev.target.closest('button[data-day]');
    if (!b) return;
    selDay = +b.dataset.day;
    const d = D.days[selDay];
    if (curZoom() !== 'day') { zoom = 'day'; renderTimeline(); }
    pin = -1;
    renderDays();
    // instant: a smooth sideways scroll would be cancelled by the page's smooth scroll up
    scrollToHour(Math.max(0, d.dlFirst - 2), false);
    $('tl-scroll').closest('section').scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  let lastCompact = null;
  window.addEventListener('resize', () => {
    if (!D) return;
    compact = window.innerWidth < 700;
    if (compact !== lastCompact) { lastCompact = compact; renderTimeline(); }
  });

  // As a home-screen app iOS keeps the page suspended and has no reload button, so the data is
  // fetched again whenever the page comes back to the front after a few minutes away.
  let loadedAt = 0;
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && (!D || Date.now() - loadedAt > 5 * 60e3)) load();
  });
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js').catch(err => console.warn('service worker:', err));
  }

  try { const s = JSON.parse(localStorage.getItem(STORE) || 'null'); if (s && s.zoom) zoom = s.zoom; } catch (e) {}
  load();

  async function load() {
    try {
      const res = await fetch('../data/klxl/pilot.json?t=' + Date.now(), { cache: 'no-store' });
      if (!res.ok) throw new Error('Fetch failed: ' + res.status);
      D = await res.json();
      loadedAt = Date.now();
      compact = lastCompact = window.innerWidth < 700;
      $('updated').textContent = 'Updated ' + D.updated;
      status();
      renderNow();
      renderTafs();
      legend();
      renderTimeline();
      renderDays();
      scrollToHour(D.nowIdx - (compact ? 3 : 8), false);
    } catch (err) {
      console.error(err);
      $('updated').textContent = 'Could not load the data.';
      const el = $('status');
      el.textContent = 'The weather data did not load (' + err.message + '). Try reloading the page.';
      el.hidden = false;
    }
  }
})();
