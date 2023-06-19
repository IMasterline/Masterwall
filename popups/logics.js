class Popup {
  constructor() {
    document.addEventListener('DOMContentLoaded', () => {
      const btblacklist = document.getElementById("btblacklist");
      btblacklist.addEventListener('click', this.blacklistWebsite);

      const btreport = document.getElementById("btreport");
      btreport.addEventListener('click', this.reportWebsite);
    });
  }

  blacklistWebsite() {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
      const xhr = new XMLHttpRequest();
      const pathArray = tabs[0].url.split('/');
      const host = pathArray[2];
      xhr.open('POST', 'http://localhost:8080/addToBlacklist/' + host, true);
      xhr.send();
    });
  }

  reportWebsite() {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
      const xhr = new XMLHttpRequest();
      const pathArray = tabs[0].url.split('/');
      const host = pathArray[2];
      xhr.open('POST', 'http://localhost:8080/addToReported/' + host, true);
      xhr.send();
    });
  }
}

const popup = new Popup();

