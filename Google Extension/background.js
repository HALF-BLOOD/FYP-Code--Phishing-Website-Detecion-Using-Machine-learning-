chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ blockedUrls: [] });
});

chrome.webRequest.onBeforeRequest.addListener(
  function (details) {
    return new Promise((resolve) => {
      chrome.storage.local.get("blockedUrls", (data) => {
        if (data.blockedUrls.includes(details.url)) {
          resolve({ cancel: true });
        } else {
          resolve({ cancel: false });
        }
      });
    });
  },
  { urls: ["<all_urls>"] },
  ["blocking"]
);
