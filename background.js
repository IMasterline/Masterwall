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


// Add an event listener
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
	// Get the URL of the new website
	var newHostname = new URL(changeInfo.url).hostname;

	// Compare with the previous hostname
	if (newHostname !== prevHostname) {
		// The user has navigated to a different website

		// Update the previous hostname variable
		prevHostname = newHostname;
	  
	  
		// Send a message to the server with the new hostname
		fetch('http://localhost:8080/update', {
			method: 'POST',
			headers: {
			'Content-Type': 'application/json'
			},
			body: JSON.stringify({hostname: newHostname})
		})
		.then(response => response.json())
		.then(data => {
			// Log the integer to the console
			console.log(`Received response: ${response}`);
			reportscount = data.reportscount;
		});
	}
	
	//on tab change: set correct popup
	changepopup();
});



//copy same code for tab on activated


chrome.runtime.onInstalled.addListener(() => {
  console.log('Service Worker installed.');
});
