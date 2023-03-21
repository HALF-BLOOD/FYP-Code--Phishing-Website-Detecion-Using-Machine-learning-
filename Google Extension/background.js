
// Store the blocked URLs in an array
var blockedUrls = [];

// Add a listener for webRequest events
chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    // Check if the URL is in the blockedUrls array
    if (blockedUrls.indexOf(details.url) !== -1) {
      // Cancel the request and redirect to the blocked page
      return {cancel: true, redirectUrl: chrome.extension.getURL("blocked.html")};
    }
  },
  {urls: ["<all_urls>"]},
  ["blocking"]
);

// Add a listener for messages from the popup
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "addBlockedUrl") {
    // Add the URL to the blockedUrls array
    blockedUrls.push(request.url);
    // Save the blockedUrls array to local storage
    chrome.storage.local.set({blockedUrls: blockedUrls}, function() {
      console.log("Blocked URLs saved.");
    });
  } else if (request.action === "getBlockedUrls") {
    // Get the blockedUrls array from local storage
    chrome.storage.local.get("blockedUrls", function(result) {
      if (result.blockedUrls) {
        blockedUrls = result.blockedUrls;
      }
      // Send the blockedUrls array back to the popup
      sendResponse({blockedUrls: blockedUrls});
    });
  }
});


blocklist.addEventListener('click', function() {
  chrome.tabs.query({currentWindow: true, active: true}, function(tabs) {
    var url = tabs[0].url;
    chrome.runtime.sendMessage({action: "addBlockedUrl", url: url}, function(response) {
      console.log(response.message);
    });
  });
});
