function shareWordEntry(target, url, title, descr, image, winWidth, winHeight) {
	var url;
	var winTop = (screen.height / 2) - (winHeight / 2);
	var winLeft = (screen.width / 2) - (winWidth / 2);
	
	event.preventDefault();
	
	switch (target) {
		case 'FACEBOOK':
			// "http://www.facebook.com/sharer.php?u=http://www.dicionariotupiguarani.com.br/dicionario/ara/"
			url = 'http://www.facebook.com/sharer.php?s=100&p[title]=' + title + '&p[summary]=' + descr + '&p[url]=' + url + '&p[images][0]=' + image;
			break;
		case 'TWITTER':
			url = 'https://twitter.com/share?url=' + url + '&amp;text=Word%20Entry%20Text&amp;hashtags=dicionariotupiguarani';
			break;
		case 'GOOGLE':
			url = 'https://plus.google.com/share?url=' + url;
			break;
	}
	
	window.open(url, 'sharer', 'top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);
}