//variables
var score = 10
var isblacklisted = 0
//on tab change: set correct popup
chrome.tabs.onActivated.addListener(function (changepopup) {
	
	
	chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    // use `url` here inside the callback because it's asynchronous!
	
	var xhr = new XMLHttpRequest();
	var pathArray = tabs[0].url.split( '/' );
	var host = pathArray[2];
	xhr.open('post','http://localhost:8080/checkBlacklist/' + host, true);
	xhr.send();
	
	
	
	
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



chrome.runtime.onInstalled.addListener(() => {
  console.log('Service Worker installed.');
});


