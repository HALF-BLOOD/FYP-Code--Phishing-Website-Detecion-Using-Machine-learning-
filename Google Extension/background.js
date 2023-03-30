// background.js

chrome.webNavigation.onCommitted.addListener((details) => {
  if (details.frameId === 0) {
    const url = details.url;
    checkForPhishing(url);
  }
});

function checkForPhishing(url) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://127.0.0.1:5000/check-phishing");
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.onload = function () {
    if (xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      var isPhishing = response.is_phishing;

      if (isPhishing) {
        // Block the phishing website
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
          chrome.tabs.update(tabs[0].id, { url: "chrome://blocked/" });
        });
      }
    }
  };
  xhr.send(JSON.stringify({ url: url }));
}