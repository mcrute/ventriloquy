#!/usr/bin/env python
# vim: set filencoding=utf8
"""
Website Build Script

@author: Mike Crute (mcrute@ag.com)
@organization: American Greetings Interactive
@date: June 03, 2010

TODO:
    * Site Map Builder
    * Full Blog Builder
        * Index page
        * Archive page
        * Feeds
"""
import sys

from os.path import dirname, realpath
sys.path.insert(0, dirname(dirname(realpath(__file__))))
del dirname, realpath

from site_builder import build_all
from site_builder.blogbuilder import build_blog

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) != 3:
        print "{0} (blog|site) input_dir output_dir".format(sys.argv[0])
        sys.exit(1)
    else:
        action, input_dir, output_dir = args

    if action == 'site':
        build_all(input_dir, output_dir)
    elif action == 'blog':
        build_blog(input_dir, output_dir)
