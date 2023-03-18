// Set up a listener for web requests
chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    // Check if the request matches a blocked URL
    if (blockedUrls.includes(details.url)) {
      console.log('Blocking URL:', details.url);
      return {cancel: true};
    }
  },
  {urls: ['<all_urls>']},
  ['blocking']
);

// Make a request to the Flask server to check if the website is phishing
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  if (changeInfo.status === 'loading' && tab.url) {
    fetch('http://localhost:5000/check-phishing', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({url: tab.url})
    })
    .then(response => response.json())
    .then(data => {
      if (data.is_phishing) {
        console.log('Phishing site detected:', tab.url);
        blockedUrls.push(tab.url);
        // Save the blocked URL to local storage
        chrome.storage.local.set({blockedUrls: blockedUrls});
        // Show a warning to the user
        chrome.notifications.create({
          type: 'basic',
          iconUrl: 'Images/power.png',
          title: 'Phishing Site Detected',
          message: 'The website you are trying to access is a known phishing site and has been blocked.'
        });
      }
    });
  }
});

// Load the blocked URLs from local storage
let blockedUrls = [];

chrome.storage.local.get(['blockedUrls'], function(result) {
  if (result.blockedUrls) {
    blockedUrls = result.blockedUrls;
  }
});
