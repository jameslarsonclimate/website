/* Home-screen app support for the WxChallenge page: registers the service worker (sw.js) and
   reloads the page when it comes back to the front after more than 5 minutes away. As a
   home-screen app iOS keeps the page suspended and has no reload button, and the page's data
   (forecast, verification, cloud context, timeline JSON) is only fetched on load, so a reload
   is what brings in the pipeline's newer runs (and a new city's page, when the city changes).
   The chosen scoreboard view and timeline switches are kept in localStorage, so they survive it. */
(function () {
  const AWAY = 5 * 60e3;
  let hiddenAt = document.visibilityState === 'hidden' ? Date.now() : 0;
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') { hiddenAt = Date.now(); return; }
    if (hiddenAt && Date.now() - hiddenAt > AWAY) location.reload();
    hiddenAt = 0;
  });
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js').catch(err => console.warn('service worker:', err));
  }

  /* Deadline reminders (Web Push, sent at 22Z by wxc_push.py on James's Mac). Only in the
     installed app (or with #remind on the URL): "Remind me" asks for permission and subscribes,
     then shows the code to add on the Mac (python wxc_push.py add), which can't be sent from
     a static page. */
  const VAPID_PUBLIC = 'BIVARQKlfAZPEJv8rKi9o_fQp64Q0uSsCbsCCYnxX5g11BqWb1ZvDcVqSbBpfG6sSz9Zuk0yoam43nPqevqyy2g';
  const box = document.getElementById('remind');
  const installed = matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  const canPush = 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window;
  if (!box || !canPush || !(installed || location.hash === '#remind')) return;
  box.hidden = false;

  const key = () => {
    const b = atob((VAPID_PUBLIC + '='.repeat((4 - VAPID_PUBLIC.length % 4) % 4)).replace(/-/g, '+').replace(/_/g, '/'));
    return Uint8Array.from(b, c => c.charCodeAt(0));
  };
  const btn = (label, fn) => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'tl-btn'; b.textContent = label;
    b.addEventListener('click', fn);
    return b;
  };
  const say = (text, ...buttons) => { box.textContent = text + ' '; buttons.forEach(b => box.append(b, ' ')); };

  async function show() {
    const reg = await navigator.serviceWorker.ready;
    const sub = await reg.pushManager.getSubscription();
    if (Notification.permission === 'denied') {
      say('🔕 Notifications are blocked for this app: turn them on in Settings › Notifications.');
    } else if (!sub) {
      say('', btn('🔔 Remind me 2 h before the deadline', on));
    } else {
      say('🔔 Deadline reminders: on for this phone.', btn('Show code', () => code(sub)),
          btn('Turn off', async () => { await sub.unsubscribe(); show(); }));
    }
  }
  async function on() {
    try {
      if (await Notification.requestPermission() !== 'granted') return show();
      const reg = await navigator.serviceWorker.ready;
      code(await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: key() }));
    } catch (err) {
      say(`Couldn't turn reminders on (${err.message}).`, btn('Try again', on));
    }
  }
  function code(sub) {
    const text = JSON.stringify(sub);
    const copy = btn('Copy code', async () => {
      try { await navigator.clipboard.writeText(text); copy.textContent = 'Copied ✓'; }
      catch (e) { copy.textContent = 'Copy failed'; }
    });
    const parts = [copy];
    if (navigator.share) parts.push(btn('Share…', () => navigator.share({ title: 'WxC reminder code', text }).catch(() => {})));
    parts.push(btn('Done', show));
    say('🔔 Last step: get this code to the Mac that sends the reminders (python wxc_push.py add).', ...parts);
  }
  show().catch(err => console.warn('reminders:', err));
})();
