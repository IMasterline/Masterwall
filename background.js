//variables
var score = 5
var isblacklisted = true

//on tab change: set correct popup
chrome.tabs.onActivated.addListener(function (changepopup) {
	if (score == 10){
		chrome.action.setPopup({ popup: "popups/safe.html"})
	}	
	if (score <= 9 && score >= 6){
		chrome.action.setPopup({ popup: "popups/risky.html"})
	}
	if (score <= 5 && score >= 2){
		chrome.action.setPopup({ popup: "popups/unsafe.html"})
	}
	if (score == 1){
		chrome.action.setPopup({ popup: "popups/scam.html"})
	}
	if (isblacklisted == true){
		chrome.action.setPopup({ popup: "popups/blacklisted.html"})
	}
});
