#!/usr/bin/python
#
# vim: tabstop=4 expandtab shiftwidth=4 autoindent
#
# template.py -- This is a template for new Python programs
#
# Copyright (C) 2005 Steve Crook <steve@mixmin.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

# The fully qualified name of the database file
dbfile = '/usr/local/news/bads/badurl/test.db'

# Are we checking headers or bodies?
look_in_headers = False

# The actual regular expression to search for.  The first bracketed group
# within it is the string we're counting.
#regex = '^NNTP\-Posting\-Host: (.*)'
#regex = '^Path: .*(?:!([\w\-]+(\.[\w\-]+)+)+)'
#regex = '^From: .*?([\w\._%+-]+\@[\w\.\-]+)'
#regex = '^Subject: \s*(?:Re:\s*)?([\x20-\x7e]+)'
regex = '(?:http:\/\/(?:www\.)?|www\.)([\w\.\-]{6,70})'

# The threshold at which we consider a URL to be excessive and blacklist it.
threshold = 500

# Ignore hits of less than this number.  This prevents the database getting
# cluttered by one-time offenders.
minimum_hits = 5

# Expire (delete) database date that is older than this number of hours.
expire_hours = 672

# The file from which to read the default list of logfiles we're going to
# process.
filelist = '/usr/local/news/bads/badurl/logfile_list'

# A list of URL's to exclude from blacklisting.
exclude = '/usr/local/news/bads/badurl/exclude_list'

# A list of URL's to manually include.
include = '/usr/local/news/bads/badurl/include_list'

# The number of bytes to read from the start of each logfile to generate a
# unique hash.  More is better but the logfile must have sufficient bytes to
# read.  Don't change this on an operational report!  A new hash will be
# generated and a false rotation will occur.
hashlength = 1000

# For some headers, such as Newsgroups, there are multiple hits per line.  If defined
# this character splits a single hit into it's elements.
element_boundary = ''

# The textfile to output.
textfile = '/usr/local/news/bads/badurl/bad_url_central'

# If we want to output regex formated entries to our text file, we should check
# they are properly escaped.
regex_safe = True

text_header = """
############################################################
# This file is downloaded from a central resource.  Do not #
# manually edit it as your changes will be overwritten     #
# during the next scheduled update.  For manual listings,  #
# update the bad_url or bad_body files.                    #
############################################################"""
