 var  bgp = chrome.extension.getBackgroundPage()
 document.addEventListener('DOMContentLoaded', function () {
    
    var btblacklist = document.getElementById("btblacklist");
    btblacklist.addEventListener('click', blacklistWebsite);
	
	var btreport = document.getElementById("btreport");
    btreport.addEventListener('click', reportWebsite);
});


function blacklistWebsite(){
	chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    // use `url` here inside the callback because it's asynchronous!
	
	var xhr = new XMLHttpRequest();
	var pathArray = tabs[0].url.split( '/' );
	var host = pathArray[2];
	xhr.open('post','http://localhost:8080/addToBlacklist/' + host, true);
	xhr.send();
	
	});
}


function reportWebsite(){
	chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    // use `url` here inside the callback because it's asynchronous!
	
	var xhr = new XMLHttpRequest();
	var pathArray = tabs[0].url.split( '/' );
	var host = pathArray[2];
	xhr.open('post','http://localhost:8080/addToReported/' + host, true);
	xhr.send();
	
	});
}
