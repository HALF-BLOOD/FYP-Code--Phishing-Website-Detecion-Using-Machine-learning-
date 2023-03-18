chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === "updatePhishingStatus") {
    var isPhishing = message.isPhishing;
    var message = message.message;
    var result = document.getElementById('result');
    var phishingStatus = document.getElementById('phishingStatus');
    if (isPhishing) {
      phishingStatus.style.color = "red";
    } else {
      phishingStatus.style.color = "green";
    }
    phishingStatus.textContent = message;
    result.innerText = isPhishing ? 'This website is a phishing website.' : 'This website is not a phishing website.';
    result.className = isPhishing ? 'result error' : 'result success';
  }
});
