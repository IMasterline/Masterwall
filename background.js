chrome.storage.local.get("score", function (isntsafe) {
	console.log(isntsafe.score)
	if (isntsafe.score == 10)
		chrome.action.setPopup({ popup: "test.html"})
});