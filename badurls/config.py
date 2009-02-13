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

# The threshold at which we consider a URL to be excessive and blacklist it.
threshold = 250

# The file from which to read the default list of logfiles we're going to
# process.
filelist = '/usr/local/news/badurls/logfile_list'

# A list of URL's to exclude from blacklisting.
exclude = '/usr/local/news/badurls/exclude_list'

# The filename used to store the persistent dictionary
dbfile = '/usr/local/news/badurls/badurl.db'

# A dictionary containing variables we need to retain between runs.
varfile = '/usr/local/news/badurls/vars.db'

# The Cleanfeed bad_url list file
cfbadurl = '/usr/local/news/cleanfeed/etc/bad_url_central'

backoff_interval = 300
backoff_rate = 1
backoff_ceiling = 1000
