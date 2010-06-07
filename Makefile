WEB_ROOT=/srv/www/crute.org/mike/htdocs

site:
	ventriloquy/metabuild.py
	rsync -auvz rendered/ $(WEB_ROOT)
	chgrp -R www-data $(WEB_ROOT)
	chmod -R g+r $(WEB_ROOT)
	find $(WEB_ROOT) -type d -exec chmod g+x {} \;

css:
	python page_source/downloads/cmpcss page_source/resources/site.css > page_source/resources/site-min.css
