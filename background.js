//variables
var score = 10
var isblacklisted = 0
//on tab change: set correct popup
chrome.tabs.onActivated.addListener(function (changepopup) {
	
	
	
	
	
	console.log(isblacklisted)
	fetch("data.json")
		.then(response => response.json())
		.then(data => {
			isblacklisted = data.isblacklisted
		});
	
	
	
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
	if (isblacklisted == 1){
		chrome.action.setPopup({ popup: "popups/blacklisted.html"})
	}
});

