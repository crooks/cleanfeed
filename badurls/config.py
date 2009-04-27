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

# Are we checking headers or bodies?
look_in_headers = False

# The actual regular expression to search for.  The first bracketed group
# within it is the string we're counting.
#regex = '^NNTP\-Posting\-Host: (.*)'
regex = '(?:http:\/\/(?:www\.)?|www\.)([\w\.\-]{10,70})'

# The threshold at which we consider a URL to be excessive and blacklist it.
threshold = 200

# Expire (delete) database date that is older than this number of hours.
expire_hours = 168

# The file from which to read the default list of logfiles we're going to
# process.
filelist = '/usr/local/news/badurl/logfile_list'

# A list of URL's to exclude from blacklisting.
exclude = '/usr/local/news/badurl/exclude_list'

# The number of bytes to read from the start of each logfile to generate a
# unique hash.  More is better but the logfile must have sufficient bytes to
# read.  Don't change this on an operational report!  A new hash will be
# generated and a false rotation will occur.
hashlength = 1000

# The textfile to output.
textfile = '/usr/local/news/badurl/bad_url_central'
