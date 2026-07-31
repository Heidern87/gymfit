const CACHE_NAME = 'gymfit-pro-v5';
const BASE = '/gymfit';
const LOCAL_URLS = [
  BASE + '/',
  BASE + '/index.html',
  BASE + '/manifest.json',
  BASE + '/icon-192x192.png',
  BASE + '/icon-512x512.png',
  BASE + '/assets/vendor/chart.umd.min.js',
  BASE + '/assets/vendor/fonts/inter-latin-400.woff2',
  BASE + '/assets/vendor/fonts/inter-latin-600.woff2',
  BASE + '/assets/vendor/fonts/inter-latin-700.woff2',
  BASE + '/assets/vendor/fonts/inter-latin-800.woff2'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(LOCAL_URLS);
    }).then(() => self.skipWaiting()).catch(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(names =>
      Promise.all(names.filter(n => n !== CACHE_NAME).map(n => caches.delete(n)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).then(response => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
        return response;
      }).catch(() => caches.match(BASE + '/index.html'))
    );
    return;
  }

  if (url.origin === location.origin) {
    event.respondWith(
      caches.match(request).then(cached => {
        if (cached) return cached;
        return fetch(request).then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
          return response;
        });
      }).catch(() => caches.match(BASE + '/index.html'))
    );
  }
});
