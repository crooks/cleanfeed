#!/usr/bin/perl -wc
# vim: shiftwidth=4 tabstop=4 autoindent smartindent smarttab

use strict;
use Digest::MD5;
our (%hdr, $modify_headers);

sub filter_post {

	# Hash the NNTP-Posting-Host header
    my $ctx = Digest::MD5->new;
	$ctx->add($hdr{'NNTP-Posting-Host'});
	$ctx->add("A touch of salt");
    $hdr{'NNTP-Posting-Host'} = $ctx->hexdigest;
	undef $hdr{'X-Trace'};

	# Modify headers for postings from the Reece Mail2News
	if ($hdr{'Mail-To-News-Contact'} =~ /abuse\@reece\.net\.au/) {
		undef $hdr{'X-Complaints-To'};
		$hdr{'Path'} = 'reece.net.au!not-for-mail';
	};

	# Refuse these From addresses
	if ($hdr{From} =~/
			\@darkshado.ca/ix) {
		return 'Sender address (From) is blacklisted';
	};

    $modify_headers = 1;
    return '';
}
