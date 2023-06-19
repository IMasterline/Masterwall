//variables
var reportscount = 0
var isblacklisted = 0
let prevHostname = "";


class PopupChanger {
  constructor(reportscount, isblacklisted) {
    this.reportscount = reportscount;
    this.isblacklisted = isblacklisted;
  }

  changePopup() {
    if (this.reportscount < 20) {
      chrome.action.setPopup({ popup: "popups/safe.html" });
    }
    if (this.reportscount >= 20 && this.reportscount < 50) {
      chrome.action.setPopup({ popup: "popups/risky.html" });
    }
    if (this.reportscount >= 50 && this.reportscount < 200) {
      chrome.action.setPopup({ popup: "popups/unsafe.html" });
    }
    if (this.reportscount > 200) {
      chrome.action.setPopup({ popup: "popups/scam.html" });
    }
    if (this.isblacklisted === 1) {
      chrome.action.setPopup({ popup: "popups/blacklisted.html" });
    }
  }
}






class TabChangeListener {
  constructor() {
    chrome.tabs.onUpdated.addListener(this.handleTabUpdated);
    chrome.tabs.onActivated.addListener(this.handleTabActivated);
  }

  handleTabUpdated(tabId, changeInfo, tab) {
    this.checkUrlChange(changeInfo.url);
  }

  handleTabActivated(activeInfo) {
    chrome.tabs.get(activeInfo.tabId, (tab) => {
      this.checkUrlChange(tab.url);
    });
  }
}

const tabChangeListener = new TabChangeListener();


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
	  })
		
		
		
	// Send a message to the server with the new hostname
      fetch('http://localhost:8080/checkBlacklist', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({hostname: newHostname})
      })
      .then(response => response.json())
      .then(data => {
        // Log the isblacklisted to the console
        console.log(`Received response: ${data.isblacklisted}`);
        isblacklisted = data.isblacklisted;
		const popupChanger = new PopupChanger(reportscount, isblacklisted);
		popupChanger.changePopup(); // Update the popup
      });
    }
  }
}




chrome.runtime.onInstalled.addListener(() => {
  console.log('Service Worker installed.');
});
