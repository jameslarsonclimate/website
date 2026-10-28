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

// deadline reminders (wxc_push.py, Web Push): show the notification; a tap opens or focuses the app
self.addEventListener('push', e => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch (err) { d = { body: e.data ? e.data.text() : '' }; }
  e.waitUntil(self.registration.showNotification(d.title || 'WxChallenge', {
    body: d.body || 'Forecast due at 00Z.', tag: d.tag || 'wxc-deadline', renotify: true,
    icon: 'icons/icon-192.png', data: { url: d.url || './' }
  }));
});
self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = new URL((e.notification.data || {}).url || './', self.registration.scope).href;
  e.waitUntil((async () => {
    for (const c of await self.clients.matchAll({ type: 'window', includeUncontrolled: true }))
      if (c.url.startsWith(self.registration.scope) && 'focus' in c) return c.focus();
    return self.clients.openWindow(url);
  })());
});
