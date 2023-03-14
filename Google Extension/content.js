// content.js

// Send a message to the background script requesting the current URL
chrome.runtime.sendMessage({request: "currentUrl"}, function(response) {
  // Display the current URL in the popup
  document.getElementById("currentUrl").textContent = response.url;
});

// background.js

// Listen for messages from the content script
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.request === "currentUrl") {
    // Get the current URL from the tab
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      var url = tabs[0].url;
      // Send the current URL back to the content script
      sendResponse({url: url});
    });
  }
  return true;
});
