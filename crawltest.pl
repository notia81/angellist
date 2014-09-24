#!/usr/bin/perl
use diagnostics;
use Spreadsheet::ParseExcel;
use Spreadsheet::WriteExcel::Big;
use WWW::Mechanize;
use HTML::Restrict;

my $mech = WWW::Mechanize->new();
$mech->get( 'https://angel.co/people/investors' );
$html=$mech->content;
open (MYFILE,'>>first.txt');
print MYFILE $html;
close(MYFILE);
$mech->click_button(value=>"More");
$html=$mech->content;
open(MYFILE,'>>second.txt');
print MYFILE $html;
close(MYFILE);

# <div class=" ds31 shared fmn96 more_pagination _a _jm" data-_tn="shared/more_pagination" data-loading_method="/people/load_more" data-object_id="people_items" data-options="{}" data-page="1" data-per_page="25" data-url="/people/investors?AL_approved=true&amp;per_page=25">&nbsp;
# </div>