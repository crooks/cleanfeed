#!/usr/bin/perl -wc
# vim: shiftwidth=4 tabstop=4 autoindent smartindent smarttab

use strict;
use Digest::MD5;
our (%hdr, $modify_headers, $user);

sub filter_post {
    my $ctx = Digest::MD5->new;
	$ctx->add($hdr{'NNTP-Posting-Host'});
	$ctx->add("Welcome to the Jungle");
    $hdr{'NNTP-Posting-Host'} = $ctx->hexdigest;
	undef $hdr{'X-Trace'};
    $modify_headers = 1;
    return '';
}
