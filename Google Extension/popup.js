document.addEventListener('DOMContentLoaded', function() {
  var checkButton = document.getElementById('checkPhishing');
  var result = document.getElementById('result');
  var urlDisplay = document.getElementById('url-display');
  var phishingButtons = document.getElementById('phishing-buttons'); // new element for phishing buttons
  var blocklist = document.getElementById('blocklist-remove'); // new element for report phishing button

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

          // Block URL if it is a phishing website
          if (isPhishing) {
            chrome.tabs.update({url: 'chrome://blocked/'});

            // Show phishing buttons if the result is phishing
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

  blocklist.addEventListener('click', function() {
    // Do something when "Report Phishing" button is clicked
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
  
        // Block URL if it is a phishing website
        if (isPhishing) {
          chrome.tabs.update({url: 'chrome://blocked/'});
        }
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
  
      // Block URL if it is a phishing website
      if (isPhishing) {
        chrome.tabs.update({url: 'chrome://blocked/'});
      }
    }
  });
  

// ---------------visual js----------------

const toggleButton = document.getElementById("toggleExtension");
const buttons = document.getElementsByTagName("button");
const checkPhishingButton = document.getElementById("checkPhishing");

toggleButton.addEventListener("click", function() {
    toggleButton.classList.toggle("on");
    toggleButton.classList.toggle("off");
    toggleButton.textContent = toggleButton.classList.contains("on") ? "ON" : "OFF";

    if (toggleButton.classList.contains("off")) {
        for (let i = 0; i < buttons.length; i++) {
            if (buttons[i] !== toggleButton) {
                buttons[i].setAttribute("disabled", "disabled");
                buttons[i].style.backgroundColor = "gray";
            }
        }
        document.body.style.backgroundColor = "gray";
        document.body.style.filter = "blur(2px)";
        checkPhishingButton.style.backgroundColor = "gray";
    } else {
        for (let i = 0; i < buttons.length; i++) {
            buttons[i].removeAttribute("disabled");
            buttons[i].style.backgroundColor = "";
        }
        document.body.style.backgroundColor = "";
        document.body.style.filter = "";
        checkPhishingButton.style.backgroundColor = "";
    }
});

