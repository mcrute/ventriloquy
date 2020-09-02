# vim: set filencoding=utf8
"""
Blog Builder

@author: Mike Crute (mike@crute.us)
@date: June 04, 2010
"""

import os
import json
import operator
from datetime import datetime
from collections import defaultdict
from site_builder import get_template, get_output_name
from blog import load_post_index
from feeds import Atom1Feed


def build_feed(output_dir, post_index, title, url, feed_url):
    page_name = os.path.join(output_dir, 'feed.atom')
    feed = Atom1Feed(post_index, title, feed_url,
                     post_index[0].post_date, url)

    open(page_name, 'w').write(feed.get_feed())


def build_tags(output_dir, post_index):
    tag_index = defaultdict(list)

    template = get_template('blog_tags.html')
    page_name = os.path.join(output_dir, 'tags.html')

    for post in post_index:
        for tag in post.tags:
            tag_index[tag].append(post)

    tag_index = sorted(tag_index.items())
    open(page_name, 'w').write(template.render(posts=tag_index,
        build_date=datetime.now().strftime("%B %d, %Y")))


def build_archive(output_dir, post_index):
    date_index = defaultdict(list)

    template = get_template('blog_archive.html')
    page_name = os.path.join(output_dir, 'archive.html')

    for post in post_index:
        date_index[post.post_date.year].append(post)

    date_index = sorted(date_index.items(), reverse=True)
    open(page_name, 'w').write(template.render(posts=date_index,
        build_date=datetime.now().strftime("%B %d, %Y")))


def build_index(output_dir, post_index):
    template = get_template('blog_index.html')
    page_name = os.path.join(output_dir, 'index.html')

    open(page_name, 'w').write(template.render(posts=post_index[:3],
        build_date=datetime.now().strftime("%B %d, %Y")))


def build_blog(base_dir, output_dir):
    config = json.load(open(os.path.join(base_dir, 'blog.cfg')))

    post_index = load_post_index(base_dir)
    post_index.sort(key=operator.attrgetter('post_date'), reverse=True)

    try:
        os.makedirs(output_dir)
    except OSError:
        pass # directory already exists 

    for post in post_index:
        template = get_template('blog_post.html')

        out_filename = os.path.join(output_dir, post.filename)
        out_filename = out_filename[:-len('rst')] + 'html'

        print "BUILDING BLOG: ", out_filename

        open(out_filename, 'w').write(template.render(post=post))

    build_index(output_dir, post_index)
    build_archive(output_dir, post_index)
    build_tags(output_dir, post_index)
    build_feed(output_dir, post_index,
                config['title'], config['blog_url'], config['feed_url'])
