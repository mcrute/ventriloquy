WEB_ROOT=/srv/www/crute.org/mike/htdocs

site: build-site sync
css: build-css sync

build-site:
	ventriloquy/metabuild.py

sync:
	rsync -auvz rendered/ $(WEB_ROOT)
	chgrp -R www-data $(WEB_ROOT)
	chmod -R g+r $(WEB_ROOT)
	find $(WEB_ROOT) -type d -exec chmod g+x {} \;

build-css:
	python downloads/cmpcss resources/site.css > resources/site-min.css
	cp resources/site-min.css rendered/resources/site-min.css
