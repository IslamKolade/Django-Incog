importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.4.1/workbox-sw.js');

workbox.setConfig({
  debug: false, // Set to true for debugging
  scope: '/', // Set the scope to cover all URLs
  headers: {
    'Service-Worker-Allowed': '/' // Add the Service-Worker-Allowed header
  }
});

workbox.routing.registerRoute(
  ({request}) => request.destination === 'image',
  new workbox.strategies.NetworkFirst()
);

workbox.routing.registerRoute(
  ({request}) => request.url.pathname === '/user/profile/edit',
  new workbox.strategies.NetworkFirst()
);

workbox.routing.registerRoute(
  ({request}) => request.url.pathname === '/',
  new workbox.strategies.NetworkFirst()
);

// Add more routes for other pages as needed
