# vim: set filencoding=utf8
"""
Blog Post Builder

@author: Mike Crute (mcrute@ag.com)
@organization: American Greetings Interactive
@date: June 03, 2010
"""

import os
from functools import wraps
from datetime import datetime

# Docutils imports, crazy yo
from docutils import nodes
from docutils.core import Publisher, publish_string
from docutils.transforms import Transform
from docutils.io import NullOutput, FileInput
from docutils.parsers.rst import Parser as RSTParser
from docutils.writers.html4css1 import Writer as HTMLWriter
from docutils.readers.standalone import Reader as StandaloneReader


class BlogMetaTransform(Transform):
    """
    Removes metadata tags from the document tree.

    This transformer removes the metadata nodes from the document tree
    and places them in a blog_meta dictionary on the document object.
    This happens before rendering so the meta won't show up in the output.
    """

    default_priority = 360 # Fuck if I know, same as the PEP header transform

    def __init__(self, *args, **kwargs):
        Transform.__init__(self, *args, **kwargs)

        self.meta = self.document.blog_meta = {
            'tags': [],
            }

    def apply(self):
        docinfo = None

        # One to get the docinfo and title
        # We need a copy of the document as a list so we can modify it
        # without messing up iteration.
        for node in list(self.document):
            if isinstance(node, nodes.docinfo):
                docinfo = node
                self.document.remove(node)

            if isinstance(node, nodes.title):
                self.meta['title'] = unicode(node[0])
                self.document.remove(node)

        # And one to process the docinfo
        for node in docinfo:
            if isinstance(node, nodes.author):
                self._handle_author(node)

            if isinstance(node, nodes.date):
                self._handle_date(node)

            if isinstance(node, nodes.field):
                self._handle_field(node)

    def _handle_author(self, node):
        self.meta['author'] = Author(node[0]['name'], node[0]['refuri'])

    def _handle_date(self, node):
        raw_date = unicode(node[0])
        self.meta['post_date'] = datetime.strptime(raw_date,
                                                    '%a %b %d %H:%M:%S %Y')

    def _handle_field(self, node):
        name = node[0][0]
        value = unicode(node[1][0][0])

        if name == 'Tag':
            self.meta['tags'].append(value)



class BlogPostReader(StandaloneReader):
    """
    Post reader for blog posts.

    This exists only so that we can append our custom blog
    transformers on to the regular ones.
    """

    def get_transforms(self):
        return StandaloneReader.get_transforms(self) + [
            BlogMetaTransform,
            ]


class Author(object):
    """
    Representation of the author information for a blog post.
    """

    def __init__(self, name, email):
        self.name = name
        self.email = email

        if email.startswith('mailto:'):
            self.email = email[len('mailto:'):]

    def __str__(self):
        return '{0} <{1}>'.format(self.name, self.email)


class BlogPost(object):
    """
    Representation of a blog post.

    Constructed from a docutils dom version of the blog post.
    """

    def __init__(self, title, post_date, author, tags, contents=None):
        self.title = title
        self.post_date = post_date
        self.author = author
        self.tags = tags
        self.contents = contents
        self._filename = None

    @property
    def filename(self):
        return os.path.basename(self._filename)

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def pretty_date(self):
        return self.post_date.strftime("%B %d, %Y")

    @classmethod
    def from_file(cls, filename):
        """
        Loads a file from disk, parses it and constructs a new BlogPost.

        This method reflects a bit of the insanity of docutils. Basically
        this is just the docutils.core.publish_doctree function with some
        modifications to use an html writer and to load a file instead of
        a string.
        """
        pub = Publisher(destination_class=NullOutput,
                        source=FileInput(source_path=filename),
                        reader=BlogPostReader(), writer=HTMLWriter(),
                        parser=RSTParser())

        pub.get_settings() # This is not sane.
        pub.settings.traceback = True # Damnit
        pub.publish()

        meta = pub.document.blog_meta
        post = cls(meta['title'], meta['post_date'], meta['author'],
                   meta['tags'], pub.writer.parts['html_body'])

        post.filename = filename

        return post


def load_post_index(directory='.'):
    """
    Scan the current directory for rst files and build an index.
    """
    posts = []
    for filename in os.listdir(directory):
        if not filename.endswith('.rst'):
            continue

        filename = os.path.join(directory, filename)
        posts.append(BlogPost.from_file(filename))

    return posts
