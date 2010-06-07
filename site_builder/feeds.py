# vim: set filencoding=utf8
"""
Atom Feed Writer

@author: Mike Crute (mcrute@ag.com)
@organization: American Greetings Interactive
@date: June 04, 2010
"""

#from io import StringIO
from StringIO import StringIO
from xml.sax.saxutils import XMLGenerator


class SimpleXMLGenerator(XMLGenerator):

    def __init__(self, encoding='utf-8'):
        self.output = StringIO()
        XMLGenerator.__init__(self, out=self.output, encoding=encoding)

    def get_contents(self):
        return self.output.getvalue()

    def startElement(self, tag, attrs=None):
        attrs = attrs if attrs else {}
        return XMLGenerator.startElement(self, tag, attrs)

    def addElement(self, tag, contents=None, attrs=None):
        attrs = attrs if attrs else {}
        self.startElement(tag, attrs)
        if contents:
            self.characters(contents)
        self.endElement(tag)


class Atom1Feed(object):

    def __init__(self, posts, title, feed_url, updated, blog_url,
                    post_filter=None):
        self.posts = posts
        self.title = title
        self.feed_url = feed_url
        self.updated = updated
        self.blog_url = blog_url
        self.handler = SimpleXMLGenerator()

        if not post_filter:
            post_filter = lambda post: True

        self.post_filter = post_filter

    def _format_time(self, timeobj):
        return timeobj.strftime("%Y-%m-%dT%H:%M:%SZ")

    def get_feed(self):
        self.handler.startDocument()
        self.handler.startElement('feed', {
            'xmlns': 'http://www.w3.org/2005/Atom' })

        self.add_root_elements()

        for post in self.posts:
            if not self.post_filter(post):
                continue

            self.add_post(post)

        self.handler.endElement('feed')

        return self.handler.get_contents()

    def add_root_elements(self):
        self.handler.addElement('title', self.title)
        self.handler.addElement('updated', self._format_time(self.updated))
        self.handler.addElement('id', self.feed_url)
        self.handler.addElement('link', attrs={
            'rel': 'alternate',
            'type': 'text/html',
            'href': self.blog_url })
        self.handler.addElement('link', attrs={
            'rel': 'self',
            'type': 'application/atom+xml',
            'href': self.feed_url })

    def add_post(self, post):
        handler = self.handler

        handler.startElement('entry')

        handler.startElement('author')
        handler.addElement('name', post.author.name)
        handler.addElement('email', post.author.email)
        handler.endElement('author')

        post_href = '{0}/{1}'.format(self.blog_url, post.filename)

        handler.addElement('title', post.title)
        handler.addElement('link', attrs={
            'rel': 'alternate',
            'type': 'text/html',
            'href': post_href })
        handler.addElement('id', post_href)
        handler.addElement('updated', self._format_time(post.post_date))
        handler.addElement('published', self._format_time(post.post_date))

        for tag in post.tags:
            handler.addElement('category', attrs={ 'term': tag })

        handler.addElement('content', post.contents, attrs={ 'type': 'html' })

        handler.endElement('entry')
