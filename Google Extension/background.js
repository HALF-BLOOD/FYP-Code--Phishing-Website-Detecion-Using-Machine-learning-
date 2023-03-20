//background.js

var isFlaskRunning = false;
var toggleExtension = document.getElementById('toggleExtension');

function startFlask() {
  if (!isFlaskRunning) {
    chrome.runtime.sendNativeMessage('com.example.flask', {command: 'start'}, function(response) {
      if (response.result == 'success') {
        isFlaskRunning = true;
        toggleExtension.className = 'off';
        toggleExtension.textContent = 'OFF';
        console.log('Flask started');
      } else {
        console.error('Failed to start Flask');
      }
    });
  } else {
    console.log('Flask is already running');
  }
}

function stopFlask() {
  if (isFlaskRunning) {
    chrome.runtime.sendNativeMessage('com.example.flask', {command: 'stop'}, function(response) {
      if (response.result == 'success') {
        isFlaskRunning = false;
        toggleExtension.className = 'on';
        toggleExtension.textContent = 'ON';
        console.log('Flask stopped');
      } else {
        console.error('Failed to stop Flask');
      }
    });
  } else {
    console.log('Flask is already stopped');
  }
}

toggleExtension.addEventListener('click', function() {
  if (!isFlaskRunning) {
    startFlask();
  } else {
    stopFlask();
  }
});
