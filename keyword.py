''' Turns inputs into KW analysis '''

import sys
import getopt
import os.path
import pandas as pd
from bs4 import BeautifulSoup
import requests

def main(argv):
    """ Turns input files into KW analysis. """

    # set default filenames
    outputfile = 'out.csv'
    htmlfile = "output.html" # The output, as an easy to use HTML file
    filelist = []
    for i in range(1,11): 
        filelist.append(str(i) + ".csv")

    # set initial values
    p_value = 3 # the number of pages this keyword must appear on
    r_value = 20 # the worst ranking the keyword can have on each of those pages
    d_value = 30 # the maximum difficulty we want to report
    produce_html = False

    try:
        opts, args = getopt.getopt(argv,"h1:2:3:4:5:6:7:8:9:10:o:p:r:d:f")
    except getopt.GetoptError:
        print('keyword.py -1 <1.csv> -2 <2.csv> -3 <3.csv> -4 <4.csv> -5 <5.csv>',
              ' -6 <6.csv> -7 <7.csv> -8 <8.csv> -9 <9.csv> -10 <10.csv>',
              ' -o <out.csv> -p <int> -r <int> -d <int> -f')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('keyword.py -1 <1.csv> -2 <2.csv> -3 <3.csv> -4 <4.csv> -5 <5.csv>',
                  ' -6 <6.csv> -7 <7.csv> -8 <8.csv> -9 <9.csv> -10 <10.csv>',
                  ' -o <out.csv> -p <int> -r <int> -d <int> -f')
            sys.exit()
        if opt in ("-1","-2","-3","-4","-5","-6","-7","-8","-9","-10"):
            num = int(opt) - 1
            filelist[num] = arg
        if opt == "-o":
            outputfile = arg
        if opt == "-p":
            p_value = int(arg)
        if opt == "-r":
            r_value = int(arg)
        if opt == "-d":
            d_value = int(arg)
        if opt == '-f':
            produce_html = True

    kwlist = pd.DataFrame()

    for i in range(0,10):
        if os.path.exists(filelist[i]):
            try:
                kwlist = kwlist.append(pd.read_csv(filelist[i]))
            except IOError:
                print("Could not read file:", filelist[i])

    urls = kwlist["Current URL"].unique()
    kwlist = kwlist[kwlist['Current position'] <= r_value]
    kwlist = kwlist[kwlist['KD'] <= d_value]
    out = kwlist.groupby('Keyword').nunique().reset_index()
    out = out.loc[:, out.columns.intersection(['Keyword'])]
    out["Count"] = 0
    for kw in kwlist["Keyword"]:
        out.loc[out["Keyword"] == kw,"Count"] += 1
    out = out[out['Count'] >= p_value]
    out["Difficulty"] = 0
    out["Volume"] = 0
    for kw in out["Keyword"]:
        out.loc[out["Keyword"] == kw,
                "Difficulty"] = kwlist.loc[kwlist["Keyword"] == kw,
                "KD"].iloc[0]
        out.loc[out["Keyword"] == kw,
                "Volume"] = kwlist.loc[kwlist["Keyword"] == kw,
                "Volume"].iloc[0]
    out = out.sort_values(['Volume','Difficulty'], ascending = [False,True])
    html_keyword_table = "<table><tr><th>Keyword</th><th>Volume</th><th>Difficulty</th></tr>\n"

    for index, row in out.iterrows():
        print(row["Keyword"], " | ", row["Volume"], " | ", row["Difficulty"])
        html_keyword_table = html_keyword_table + "<tr><td>" + row["Keyword"] \
                             + "</td><td>" + str(row["Volume"]) + "</td><td>" \
                             + str(row["Difficulty"]) + "</td></tr>\n"

    html_keyword_table = html_keyword_table + "</html>\n"

    if produce_html:

        url_list = "<p>\n"

        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 i'\
                             '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

        for url in urls:
            if len(str(url)) > 4:
                urlbits = url.split("/")
                topurl = "http://" + urlbits[2]
                req = requests.get(topurl, hdr)
                soup = BeautifulSoup(req.content, 'html.parser')
                title = soup.find('title')
                url_list = url_list + "<strong>" + str(title.string) + "</strong>: "

                req = requests.get(url, hdr)
                soup = BeautifulSoup(req.content, 'html.parser')
                title = soup.find('title')
                url_list = url_list + "<a href=\"" + str(url) + "\">" \
                           + str(title.string) + "</a><br />\n"

        url_list = url_list + "</p>\n"

        table_html = "<html>\n<head>\n<title>Keyword Analysis</title>\n</head>\n<body>" \
                     + "\n<h2>Top 10 Pages</h2>\n" \
                     + "<p>Here are the top ten pages for your keyword.</p>\n" \
                     + url_list + "<h2>Keyword Table</h2>\n" + html_keyword_table \
                     + "</body>\n</html>"

        try:
            with open(htmlfile, 'w') as f:
                f.write(table_html)
        except IOError:
            print("Could not write file:", htmlfile)

if __name__ == "__main__":
    main(sys.argv[1:])
