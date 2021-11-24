# ahrefs-keyword-analyzer
A tool for analyzing keyword neighborhoods using organic keyword reports from Ahrefs.  It's written in python and thus runs easily from the command line:

python keyword.py

A "keyword neighborhood" is an approach for finding interesting long-tail keywords to write about based on a broad root keyword.  It's a time-saver, condensing some of the hunting and searching for related keywords down to a simpler process.  The input files do require having an Ahrefs account for initial retrieval.

The script relies on some files being present in the directory for analysis.  By default, it checks for files named 1.csv through 10.csv as well as self.csv.

1.csv through 10.csv are exported CSV files from Ahrefs that contain all of the keywords for each of the top 10 pages for your desired root keyword.  These are retrieved manually from Ahrefs before running the script.  You do not need to have ten of them, but the program is redundant if you just have one file.  

self.csv is an exported CSV file from Ahrefs that contains all keywords for an already-existing URL that you may want to rewrite.  It's not required, but can be useful if you're intending to rewrite an existing page.  

You can easily export these CSV files from Ahrefs by going to a keyword report in Ahrefs, like this one:
https://app.ahrefs.com/v2-site-explorer/organic-keywords/exact?country=us&target=https%3A%2F%2Fwww.medicalnewstoday.com%2Farticles%2F271157
and clicking on the Export button in the upper right.  Choose UTF-8 encoding.

If you have a particular root keyword, such as 'bananas,' start with the Ahrefs keyword analysis for that keyword:
https://app.ahrefs.com/keywords-explorer/google/us/overview?keyword=bananas
If you scroll down, you'll find an SERP overview for that keyword.  You can quickly jump to the organic keyword report for each of those URLs by clicking on the green arrow next to each URL you want to include and choosing "organic keywords."

By default, keyword.py creates an output.csv file in that directory that contains a comma-delimited keyword neighborhood.

# What is Ahrefs?
Ahrefs is a web service that provides detailed reports on Google keywords.  However, drawing useful conclusions from that data can sometimes be tricky.

# What is a "keyword neighborhood"?
A "keyword neighborhood" is a set of all keywords "in the neighborhood" of a given root keyword.  In my use, it's the set of all keywords for which the top pages of a given keyword rank.

Let's say you are interested in the keyword "bananas."  If you do a Google search for "bananas," you'll get a large quantity of results.  If you look at the set of all keywords for which the top ten results for "bananas" are ranking, you have the "keyword neighborhood" for bananas.

Typically, this keyword neighborhood is quite large, so we want to filter it down a little bit.

# How do we reduce the "keyword neighborhood"?
The most effective strategy is to look for keywords that the top pages have in common.  There are two variables that one can set when doing this analysis.

P is the number of top pages for the root keyword that the neighborhood keyword must rank for.
R is the minimum ranking for that neighborhood keyword on those top pages.

For example, one might want to see the list of all keywords that rank in the top 20 (R=20) on at least 3 of the top 10 pages (P=3) for "bananas."

# Why do this?
Seeing this filtered keyword neighborhood usually gives a healthy set of more specific keywords for a particular topic.  This result set is usually small enough to go through manually, enabling you to find interesting keywords.  If it's too large, you can either decrease R or increase P via command line options.

# Command line options

-p number
    set the value of P.  By default, it is half of the number of files selected for processing, rounded up.  So, if you are looking at 8 files, P defaults to 4.  Choose a higher number for a more stringent set.  Minimum is 1, maximum is 10.

-r number
    set the value of R.  By default, it is 20.  Choose a lower number for a more stringent set.  Minimum is 1, maximum is 100.

-1 file
-2 file
...
-10 file
    set the file names and locations of your CSV files.  By default, they are assumed to be '1.csv' through '10.csv' in the same directory.  You do not need to have all ten; the script will identify which ones you have and adjust accordingly.

-s file
    set the file name of the 'self' file.  By default, it's assumed to be self.csv.  You do not need to have this file, the script adjusts based on whether the file is present.
