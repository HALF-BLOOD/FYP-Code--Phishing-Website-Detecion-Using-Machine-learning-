document.addEventListener('DOMContentLoaded', function() {
  var checkButton = document.getElementById('checkPhishing');
  var result = document.getElementById('result');
  var urlDisplay = document.getElementById('url-display');
  var phishingButtons = document.getElementById('phishing-buttons');

  checkButton.addEventListener('click', function() {
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs) {
      var url = tabs[0].url;
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "http://127.0.0.1:5000/check-phishing");
      xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      xhr.onload = function() {
        if (xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          var isPhishing = response.is_phishing;
          result.innerText = isPhishing ? 'This website is a phishing website.' : 'This website is not a phishing website.';
          result.className = isPhishing ? 'result error' : 'result success';

          // Redirect to blocked page and show phishing buttons if the result is phishing
          if (isPhishing) {
            chrome.storage.local.set({originalUrl: url}); // Store the original URL in the local storage
            chrome.tabs.update({url: 'chrome://blocked/'});
            phishingButtons.style.display = "block";
          }
        } else {
          result.innerText = 'There was an error checking for phishing.';
          result.className = 'result error';
        }
      };
      xhr.send(JSON.stringify({url: url}));

      // Display the URL in the popup
      urlDisplay.textContent = 'Checking URL: ' + url;
    });
  });
});

document.getElementById("yesButton").addEventListener("click", function () {
  chrome.storage.local.get('originalUrl', function(data) { // Get the original URL from the local storage
    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
      if (data.originalUrl) {
        chrome.tabs.update(tabs[0].id, { url: data.originalUrl });
      }
    });
  });
});

document.getElementById("noButton").addEventListener("click", function () {
  chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    chrome.tabs.update(tabs[0].id, { url: "chrome://blocked/" });
  });
});