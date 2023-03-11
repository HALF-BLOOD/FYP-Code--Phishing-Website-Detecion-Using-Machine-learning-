chrome.browserAction.onClicked.addListener(function(tab) {
  chrome.tabs.query({currentWindow: true, active: true}, function(tabs) {
    var url = tabs[0].url;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/check-phishing");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({url: url}));
  });
});
