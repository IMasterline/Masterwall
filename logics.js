function reportWebsite(){
	var xhr = new XMLHttpRequest();
	xhr.open('post','http://localhost:8080/addToBlacklist/' + tab.url, true);
	xhr.send();
}
reportWebsite();
