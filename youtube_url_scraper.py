# youtube url scraper -- Classy @ HF
# requirements: python 2.7.X and Requests

import sys
import os.path
import requests
import re

def get_ch_html(url):
    req = requests.get(url)
    return req.text


def scrape(url, channel):
    index = 1
    found = 0
    retlist = []
    print "[!] Scraping..\n"

    while 1:
        videoshtml = get_ch_html(url % (channel, index))
        #re_pattern = "\/watch\?(?=.*v=\w+)(?:\S+)\""
        re_pattern = "a href=\"http://www.youtube.com/watch\?v=(.*?)&amp;"
        reg = re.compile(re_pattern)
        m = reg.findall(videoshtml)
        found += len(m)
        retlist.extend(m)
        if len(m) == 0:
            print "[+] Scraping ended."
            break
        index += 50
    print "[!] Videos found:", found
        
    return retlist

def modurls(scrapelist):
    retlist = []
    for x in scrapelist:
        retlist.append("http://youtube.com/watch?v=" + x)
    return retlist

def filesave(scrapelist):
    filename = raw_input("Enter filename to save as (including .txt): ")
    while os.path.isfile(filename):
        print "File already exists! We don't want to overwrite it!"
        filename = raw_input("Enter a different filename: ")

    if filename == "":
        filename = "videolist.txt"
    f = open(filename, 'w')

    f.write("Videos found: %d\n" % int(len(scrapelist)))
    for line in scrapelist:
        f.write(line + '\r\n')
    f.close()

def main():
    print "Youtube URL scraper by Classy @ HF"
    channel = raw_input("Channel name: ")
    url = "http://gdata.youtube.com/feeds/base/users/%s/uploads?max-results=50&start-index=%d"
    urls = scrape(url, channel)
    urls = modurls(urls)
    filesave(urls)

    print "Looks like scraper executed successfully!"
    print "Terminating.."
    return 0

if __name__ == "__main__":
    sys.exit(main())
