# vim: set filencoding=utf8
"""
Site Builder

@author: Mike Crute (mcrute@ag.com)
@organization: American Greetings Interactive
@date: June 04, 2010
"""

import os
import jinja2
import pagebuilder
from datetime import datetime
from docutils.core import publish_parts
from docutils.io import FileInput


def get_template(name):
     loader = jinja2.FileSystemLoader('ventriloquy/templates')
     renderer = jinja2.Environment(loader=loader)
     return renderer.get_template(name)


def build_standard_page(filename, output_name):
    parts = publish_parts(open(filename, 'r').read(), writer_name='html')
    template = get_template('page.html')

    try:
        os.makedirs(os.path.dirname(output_name))
    except OSError:
        pass # directory exists

    open(output_name, 'w').write(template.render(
        contents=parts['html_body'],
        build_date=datetime.now().strftime('%B %d, %Y'),
        source_link=filename))


def get_output_name(base_dir, output_dir, filename):
    base_depth = len(base_dir.split(os.path.sep))
    out_name = filename.split(os.path.sep)[base_depth:]
    new_path = os.path.join(output_dir, *out_name)

    if new_path.endswith('.rst'):
        new_path = new_path[:-len('.rst')] + '.html'

    return new_path


def build_all(base_dir, output_dir):
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if ('personal_blog' in root or
                'blog' in root or
                not filename.endswith('.rst')):
                continue

            old_path = os.path.join(root, filename)
            new_path = get_output_name(base_dir, output_dir, old_path)

            print "BUILDING: ", old_path

            build_standard_page(old_path, new_path)
