document.addEventListener('DOMContentLoaded', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      var url = tabs[0].url;
      var urlElement = document.getElementById('url');
      urlElement.textContent = url;
    });
  });
  