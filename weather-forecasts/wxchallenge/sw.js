/* WxChallenge page service worker: network first, so the page and data are always the newest
   when there's a connection; the last good copy is shown only when there isn't (the page's
   "Last updated" line then shows how old it is). Only this page's own files are kept;
   everything else (images, other pages) goes straight to the network. */
const CACHE = 'wxc-v1';
const KEEP = ['./', 'index.html', 'timeline.js', 'app.js', 'manifest.webmanifest', 'icons/icon-192.png',
              'icons/apple-touch-icon.png', 'icons/favicon-32.png',
              '../data/wxchallenge/forecast.json', '../data/wxchallenge/verification.json',
              '../data/wxchallenge/cloud_context.json', '../data/wxchallenge/timeline.json'];
const keepUrls = KEEP.map(p => new URL(p, self.registration.scope).pathname);

self.addEventListener('install', e => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil((async () => {
  for (const k of await caches.keys()) if (k !== CACHE) await caches.delete(k);
  await self.clients.claim();
})()));

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin || !keepUrls.includes(url.pathname)) return;
  e.respondWith((async () => {
    const key = url.origin + url.pathname;          // the data is fetched with ?t=...
    try {
      const res = await fetch(e.request);
      if (res.ok) (await caches.open(CACHE)).put(key, res.clone());
      return res;
    } catch (err) {
      const hit = await caches.match(key);
      if (hit) return hit;
      throw err;
    }
  })());
});
