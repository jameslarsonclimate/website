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
})();
