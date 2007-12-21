#!/usr/bin/perl -wc
# vim: shiftwidth=4 tabstop=4 autoindent smartindent smarttab

use strict;
our (%hdr, $modify_headers, $user);

sub filter_post {
    my @delete_headers = qw(NNTP-Posting-Host X-Trace);

    if ($user eq 'md@newsguests') {
        push(@delete_headers, qw(Sender X-Complaints-To));
    }

    $hdr{$_} = undef foreach @delete_headers;
    $modify_headers = 1;
	
    return '';
}
