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
            chrome.tabs.update({url: 'redirect.html'});
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
  chrome.storage.local.get('originalUrl', function(data) {
    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
      if (data.originalUrl) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http://127.0.0.1:5000/remove-from-hosts");
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({url: data.originalUrl}));
        chrome.tabs.update(tabs[0].id, { url: data.originalUrl });
      }
    });
  });
});


document.getElementById("noButton").addEventListener("click", function () {
  chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    chrome.tabs.update(tabs[0].id, { url: "Thankyou.html" });
  });
});



document.getElementById("blockedUrl").addEventListener("click", function () {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "http://127.0.0.1:5000/blocked-urls");
  xhr.onload = function () {
    if (xhr.status === 200) {
      var blockedUrls = JSON.parse(xhr.responseText);
      displayBlockedUrls(blockedUrls); // Add this line to call the function
    } else {
      console.error("Error fetching blocked URLs");
    }
  };
  xhr.send();
});

function unblockUrl(url, rowElement) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://127.0.0.1:5000/remove-from-hosts");
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.onload = function () {
    if (xhr.status === 204) {
      // Remove the URL from the table
      rowElement.parentNode.removeChild(rowElement);
    } else {
      console.error("Error unblocking URL");
    }
  };
  xhr.send(JSON.stringify({ url: url }));
}


function displayBlockedUrls(blockedUrls) {
  var table = document.createElement("table");
  var thead = document.createElement("thead");
  var headerRow = document.createElement("tr");

  var urlHeader = document.createElement("th");
  urlHeader.textContent = "URL";
  headerRow.appendChild(urlHeader);

  var unblockHeader = document.createElement("th");
  unblockHeader.textContent = "Unblock";
  headerRow.appendChild(unblockHeader);

  thead.appendChild(headerRow);
  table.appendChild(thead);

  var tbody = document.createElement("tbody");

  blockedUrls.forEach(function (url) {
    var tr = document.createElement("tr");

    var urlCell = document.createElement("td");
    urlCell.textContent = url;
    tr.appendChild(urlCell);

    var unblockCell = document.createElement("td");
    var unblockButton = document.createElement("button");
    unblockButton.textContent = "Unblock";
    unblockButton.addEventListener("click", function () {
      unblockUrl(url, tr);
    });
    unblockCell.appendChild(unblockButton);
    tr.appendChild(unblockCell);

    tbody.appendChild(tr);
  });

  table.appendChild(tbody);
  document.body.appendChild(table);
}

