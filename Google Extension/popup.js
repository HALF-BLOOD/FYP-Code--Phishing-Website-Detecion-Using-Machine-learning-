// Create a function that gets the current URL
function getCurrentUrl() {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    // Get the URL from the active tab
    var url = tabs[0].url;
    // Call the function to update the URL in the popup
    updateUrl(url);
  });
}

// Create a function that updates the URL in the popup
function updateUrl(url) {
  document.getElementById('url').innerText = url;
}

// Add an event listener for when the power button is clicked
document.getElementById('power').addEventListener('click', function() {
  // Send a message to the background script to close the current tab
  chrome.runtime.sendMessage({action: 'closeCurrentTab'});
  // Update the URL in the popup
  updateUrl("Tab closed");
});

// Call the getCurrentUrl function when the popup is opened
document.addEventListener('DOMContentLoaded', function() {
  getCurrentUrl();
});

chrome.runtime.sendMessage({action: 'getCurrentUrl'}, function(response) {
  // Send the current URL to the Python code
  sendUrlToPython(response.url);
});
