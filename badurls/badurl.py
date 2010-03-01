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

import config
import datetime
import hashlib
import os.path
import re
import sys
from pysqlite2 import dbapi2 as sqlite

def CommandArgs(args):
    """Check arguements passed on the command line"""
    if len(args) > 1:
        if args[1].startswith('--'):
            option = args[1] [2:]
            if len(args) > 2:
                content = args[2]
                return option, content
            return True, None
    return False, None

def CheckTables():
    """Check if a given tablename exists.  If not, create it."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    if not tables or not "master" in tables:
        cursor.execute('''CREATE TABLE master (
            hit TEXT,
            logfile TEXT,
            count INTEGER,
            date TEXT)''')
        con.commit()
    if not tables or not "rotate" in tables:
        cursor.execute('''CREATE TABLE rotate (
            logfile TEXT,
            hash TEXT,
            date TEXT)''')
        con.commit()

def HasRotated(logfile, hash):
    """Try and decide if the specified logfile has rotated since the script
    was last executed."""
    timestamp = utcnow()
    cursor.execute('''SELECT hash, date FROM rotate
                      WHERE logfile = "%s"''' % (logfile,))
    result = cursor.fetchone()
    # If the database doesn't have an entry for our logfile then we need to
    # create one for it using the passed logfile hash and the current
    # timestamp.
    if not result:
        print "New logfile, adding hash and date."
        cursor.execute('''INSERT INTO rotate (logfile, hash, date)
                    VALUES ("%s", "%s", "%s")''' % (logfile, hash, timestamp))
        con.commit()
        return timestamp
    if result[0] == hash:
        # The current logfile hash matches the recorded one at last rotation,
        # we just return the old timestamp.
        return result[1]
    # If we get here, the logfile hash is different, indicating that rotation
    # has occured. We therefore set and return a new timestamp.
    print logfile, "has rotated"
    cursor.execute('''UPDATE rotate SET hash = "%s", date = "%s"
                      WHERE logfile = "%s"''' % (hash, timestamp, logfile))
    con.commit()
    return timestamp
     
def DB_Exists(logfile, timestamp):
    """Return True if our master table already contains an entry for hit and
    logfile."""
    cursor.execute('''SELECT hit FROM master
                      WHERE logfile = "%s"
                      AND date = "%s"''' % (logfile, timestamp))
    exists = [row[0] for row in cursor.fetchall()]
    return exists

def DB_Insert(hit, logfile, count, timestamp):
    """Insert a new entry into our master table."""
    items = { 'hit'     :   hit.replace("'","''"),
              'logfile' :   logfile,
              'count'   :   count,
              'date'    :   timestamp }
    cursor.execute('''INSERT INTO master (hit, logfile, count, date)
                        VALUES (
                        '%(hit)s',
                        '%(logfile)s',
                        %(count)s,
                        '%(date)s')''' % items)
    con.commit()

def DB_Update(hit, logfile, count, timestamp):
    items = { 'hit'     :   hit.replace("'","''"),
              'logfile' :   logfile,
              'count'   :   count,
              'date'    :   timestamp }
    cursor.execute('''UPDATE master SET count = %(count)s
                      WHERE hit = '%(hit)s'
                      AND logfile = '%(logfile)s'
                      AND date = '%(date)s' ''' % items)
    con.commit()

def DB_Read():
    cursor.execute('''SELECT hit, sum(count) as total FROM master
                    GROUP BY hit ORDER BY total''')
    return cursor.fetchall()

def DB_Delete(hit):
    count = cursor.execute('''DELETE FROM master WHERE hit = '%s' ''' % hit).rowcount
    con.commit()
    return count

def DB_Expire(hours):
    cursor.execute('''SELECT COUNT(hit) FROM master WHERE
       datetime(date) < datetime("%s")''' % (hours_ago(hours),))
    expire = cursor.fetchone()
    cursor.execute('''DELETE FROM master WHERE
       datetime(date) < datetime("%s")''' % (hours_ago(hours),))
    con.commit()
    return expire[0]

def utcnow():
    """Just return the utc time.  Everything should work on utc."""
    utctime = datetime.datetime.utcnow()
    utcstamp = utctime.strftime("%Y-%m-%d %H:%M:%S")
    return utcstamp

def hours_ago(past_hours):
    """ Like utcnow() but return a timestamp for a given number of hours in
    the past."""
    thentime = datetime.datetime.utcnow() - datetime.timedelta(hours=past_hours)
    return thentime.strftime("%Y-%m-%d %H:%M:%S")

def File2List(filename):
    """Read a file and return each line as a list item."""
    items = []
    if IsFile(filename):
        readlist = open(filename, 'r')
        for line in readlist:
            if not line.startswith('#') and len(line) > 1:
                items.append(line.rstrip())
    return items

def IsFile(filename):
    """Return True is a passed filename exists and is a normal file."""
    if os.path.isfile(filename):
        return True
    sys.stdout.write("%s: Not a valid file\n" % (filename,))
    return False

def GetSize(filename):
    """Return the size of a given file in Bytes"""
    return os.path.getsize(filename)

def Excluded(entry, list_to_exclude):
    """Compare a passed entry with all the entries in the exclude list.
    Entries will be treated as plain text unless wrapped within slashes in
    which case they will be regarded as regex's."""
    excluded = False
    for rule in list_to_exclude:
        # Entries wrapped in /.../ are regex format.
        if rule.startswith('/') and rule.endswith('/'):
            # Strip the first and last chars.
            rule = rule[1:-1]
            if re.search(rule, entry, re.IGNORECASE):
                excluded = True
                break
        # If entry is not regex, do a plain-text compare.
        else:
            lcentry = entry.lower()
            if lcentry.find(rule) >= 0:
                excluded = True
                break
    return excluded

def RegexSafe(regex):
    """Manipulate a passed fqdn to make it regex friendly"""
    regex = regex.lower()
    regex = regex.replace('.', '\.')
    regex = regex.replace('-', '\-')
    # This should never happen but best to be careful.
    regex = regex.replace('||', '|')
    return regex


def ScanFiles(files):
    """Read a list of files.  Return an occurances count of each individual
    regex match contained within those files."""
    # The following line might need some tweeking for specific applications.
    if config.look_in_headers:
        regex = re.compile(config.regex)
    else:
        regex = re.compile(config.regex, re.I | re.M)
    # The following two regexs match the beginning and end of mbox articles
    from_regex = re.compile('From foo\@bar', re.M)
    empty_regex = re.compile('^$')
    for filename in files:
        if IsFile(filename):
            print "Scanning", filename
            # We can't risk not having enough bytes to hash, this would result
            # in a false logfile rotation as the logfile grew.
            if GetSize(filename) < config.hashlength:
                print "File to small to hash, ignoring."
                continue

            # Open the logfile
            file = open(filename, 'r')

            # Now the file is open, we generate a hash of its first 500 bytes.
            # The hash is later used to decide if the logfile has rotated.
            fingerprint = file.read(config.hashlength)
            # Reset marker to beginning of file.
            file.seek(0)
            hash = hashlib.sha1(fingerprint).hexdigest()
            timestamp = HasRotated(filename, hash)

            # onbody toggles as we switch between headers and body in our
            # logfile.
            onbody = False
            # hits is a dictionary of regex matches containing a hit count.
            hits = {}
            # From this point we are dealing with lines within a logfile.
            for line in file:
                line = line.strip()
                # Two checks to determine if we're looking at headers or body
                if empty_regex.match(line) and not onbody:
                    onbody = True
                    continue
                if from_regex.match(line) and onbody:
                    onbody = False
                    continue
                # Are we processing headers or body
                if onbody and config.look_in_headers:
                    continue
                if not onbody and not config.look_in_headers:
                    continue
                test = regex.search(line)
                if test:
                    match = test.group(1).lower()
                    # If we have configured an element boundary then use it,
                    # otherwise just create a single-item list.
                    if config.element_boundary:
                        elements = match.split(config.element_boundary)
                    else:
                        elements = [match]
                    for element in elements:
                        element = element.strip()
                        if element in hits:
                            hits[element] += 1
                        else:
                            hits[element] = 1
            existing = DB_Exists(filename, timestamp)
            for hit in hits:
                # If a hit is excluded or its count hasn't reached a minimal
                # level since last rotation, ignore it.
                if hits[hit] < config.minimum_hits:
                    continue
                if hit not in existing:
                    print "Inserting %s into %s" % (
                        hit,
                        filename.split('/').pop()
                    )
                    DB_Insert(hit, filename, hits[hit], timestamp)
                else:
                    DB_Update(hit, filename, hits[hit], timestamp)
            file.close()

def ProcessLogfiles():
    # Logfiles to be read by default.  This can be overridden by command line args.
    logfiles = File2List(config.filelist)
    # URL's to exclude from processing.  Entries can be plain-text or regex.
    exclude = File2List(config.exclude)
    include = File2List(config.include)

    # Run the expiry process to get rid of any entries over expire_hours old.
    print "Expired: ", DB_Expire(config.expire_hours)


    ScanFiles(logfiles)
    results = DB_Read()

    # Prepare to overwrite Cleanfeed's bad_url_central file.
    badurl = open(config.textfile, 'w')
    badurl.write(config.text_header.lstrip())
    badurl.write('\n\n')
    badurl.write('# Last Updated: %s\n\n' % (utcnow(),))

    # First, process the entries in our manual include file.
    for hit in include:
        if hit.startswith('/') and hit.endswith('/'):
            hit = hit[1:-1]
        elif config.regex_safe:
            hit = RegexSafe(hit)
        badurl.write("%-40s # Manually included\n" % (hit,))
        print "%-40s Manually included" % (hit,)

    # Next process everything not Manually included.
    for hit, count in results:
        if count > config.threshold:
            exc = Excluded(hit, exclude)
            inc = Excluded(hit, include)
            # Regex Safe mode ensures text output is escaped.
            if config.regex_safe:
                hit = RegexSafe(hit)
            #else:
            #    entry = hit
            if not inc and not exc:
                badurl.write("%-40s # %d\n" % (hit, count))
                print "%-40s %d" % (hit, count)
            elif inc and not exc:
                badurl.write("#%-39s # %d Matches manual list\n" % (hit, count))
                print "# %-38s %d Matches manual list" % (hit, count)
            elif not inc and exc:
                badurl.write("#%-39s # %d Whitelisted\n" % (hit, count))
                print "# %-38s %d Whitelisted" % (hit, count)
            else:
                badurl.write("#%-39s # %d Error: Matches Include and Exclude\n" % (hit, count))
                print "# %-38s %d Error: Matches Include and Exclude" % (hit, count)
    # Close the file and shelves
    badurl.close()


def Main():
    global con
    con = sqlite.connect(config.dbfile)
    global cursor
    cursor = con.cursor()
    # Check tables exist
    CheckTables()

    cmd, opt = CommandArgs(sys.argv)
    if not cmd:
        ProcessLogfiles()
    elif cmd and opt:
        if cmd == 'insert':
            DB_Insert(opt, "Manual", 10000, utcnow())
        if cmd == 'delete':
            count = DB_Delete(opt)
            if count:
                print "Deleted: %d" % count


if (__name__ == "__main__"):
    Main()
