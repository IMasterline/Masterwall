//variables
var score = 5
var isblacklisted = false

//on tab change: set correct popup
chrome.tabs.onActivated.addListener(function (changepopup) {
	
	
	chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    // use `url` here inside the callback because it's asynchronous!
	
	var xhr = new XMLHttpRequest();
	var pathArray = tabs[0].url.split( '/' );
	var host = pathArray[2];
	xhr.open('post','http://localhost:8080/checkBlacklist/' + host, true);
	xhr.send();
	var data = JSON.parse(xhr.responseText);
	
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
	if (isblacklisted == true){
		chrome.action.setPopup({ popup: "popups/blacklisted.html"})
	}
});

