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

if __name__ == '__main__':
    from site_builder import build_all
    from site_builder.blogbuilder import build_blog
    build_all('page_source', 'rendered')
    build_blog('page_source/blog', 'rendered/blog')
    build_blog('page_source/personal_blog', 'rendered/personal_blog')
