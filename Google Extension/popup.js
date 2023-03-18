document.addEventListener('DOMContentLoaded', function() {
  var checkButton = document.getElementById('checkPhishing');
  var result = document.getElementById('result');

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
        } else {
          result.innerText = 'There was an error checking for phishing.';
          result.className = 'result error';
        }
      };
      xhr.send(JSON.stringify({url: url}));
    });
  });
});

document.addEventListener('DOMContentLoaded', function() {
    var checkPhishingButton = document.getElementById('checkPhishingButton');
    var phishingStatus = document.getElementById('phishingStatus');
  
    checkPhishingButton.addEventListener('click', function() {
      chrome.runtime.sendMessage({action: "getPhishingStatus"}, function(response) {
        var isPhishing = response.isPhishing;
        var message = response.message;
        if (isPhishing) {
          phishingStatus.style.color = "red";
        } else {
          phishingStatus.style.color = "green";
        }
        phishingStatus.textContent = message;
      });
    });
  });
  

  chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action == "sendPhishingStatus") {
      var isPhishing = request.isPhishing;
      var message = request.message;
      var phishingStatus = document.getElementById('phishingStatus');
      if (isPhishing) {
        phishingStatus.style.color = "red";
      } else {
        phishingStatus.style.color = "green";
      }
      phishingStatus.textContent = message;
    }
  });
  
