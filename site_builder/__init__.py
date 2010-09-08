# vim: set filencoding=utf8
"""
Site Builder

@author: Mike Crute (mcrute@ag.com)
@organization: American Greetings Interactive
@date: June 04, 2010
"""

import os
from os import path
import jinja2
import pagebuilder
from datetime import datetime
from docutils.core import publish_parts
from docutils.io import FileInput


TEMPLATES = path.join(path.dirname(path.dirname(__file__)), "templates")


def get_template(name):
    loader = jinja2.FileSystemLoader(TEMPLATES)
    renderer = jinja2.Environment(loader=loader)
    return renderer.get_template(name)


def build_standard_page(filename, output_name):
    parts = publish_parts(open(filename, 'r').read(), writer_name='html')
    template = get_template('page.html')

    try:
        os.makedirs(path.dirname(output_name))
    except OSError:
        pass # directory exists

    open(output_name, 'w').write(template.render(
        contents=parts['html_body'],
        build_date=datetime.now().strftime('%B %d, %Y'),
        source_link=filename))


def get_output_name(base_dir, output_dir, filename):
    base_depth = len(base_dir.split(path.sep))
    out_name = filename.split(path.sep)[base_depth:]
    new_path = path.join(output_dir, *out_name)

    if new_path.endswith('.rst'):
        new_path = new_path[:-len('.rst')] + '.html'

    return new_path


def build_all(base_dir, output_dir):
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if ('blog.cfg' in files or
                not filename.endswith('.rst')):
                continue

            old_path = path.join(root, filename)
            new_path = get_output_name(base_dir, output_dir, old_path)

            print "BUILDING: ", old_path

            build_standard_page(old_path, new_path)
