//variables
var reportscount = 0
var isblacklisted = 0
let prevHostname = "";


function changepopup() {
	
	if (reportscount == 0){
		chrome.action.setPopup({ popup: "popups/safe.html"})
	}	
	if (reportscount == 1){
		chrome.action.setPopup({ popup: "popups/risky.html"})
	}
	if (reportscount == 2){
		chrome.action.setPopup({ popup: "popups/unsafe.html"})
	}
	if (reportscount == 3){
		chrome.action.setPopup({ popup: "popups/scam.html"})
	}
	if (isblacklisted == 1){
		chrome.action.setPopup({ popup: "popups/blacklisted.html"})
	}
}





// Add event listeners for URL changes and tab changes
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  checkUrlChange(changeInfo.url);
});

chrome.tabs.onActivated.addListener((activeInfo) => {
  chrome.tabs.get(activeInfo.tabId, (tab) => {
    checkUrlChange(tab.url);
  });
});

// Define a function to check for URL changes
function checkUrlChange(url) {
  if (url) {
    // Get the hostname of the new website
    var newHostname = new URL(url).hostname;

    // Compare with the previous hostname
    if (newHostname !== prevHostname) {
      // The user has navigated to a different website

      // Update the previous hostname variable
      prevHostname = newHostname;

      // Send a message to the server with the new hostname
      fetch('http://localhost:8080/checkReported', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({hostname: newHostname})
      })
      .then(response => response.json())
      .then(data => {
        // Log the reportscount to the console
        console.log(`Received response: ${data.reportscount}`);
        reportscount = data.reportscount;
      });
    }
  }

  // Update the popup
  changepopup();
}




chrome.runtime.onInstalled.addListener(() => {
  console.log('Service Worker installed.');
});
