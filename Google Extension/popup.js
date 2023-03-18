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
