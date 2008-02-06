#!/usr/bin/python
#
# vim: tabstop=4 expandtab shiftwidth=4 autoindent
#
# badhosts.py -- Auto-management of the cleanfeed bad_hosts file
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

# Filename for the badhosts database file
# TODO This needs to be fully qualified for release versions
dbfile = 'badhosts.db'

threshold = 200

report_file = '/usr/local/news/cleanfeed/log/PHR.EMP'

