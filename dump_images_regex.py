"""
dumpimages.py
    Downloads all the images on the supplied URL, and saves them to the
    specified output file ("/test/" by default)

Usage:
    python dumpimages.py http://example.com/ [output]
"""

from bs4 import BeautifulSoup as bs
import shutil
import urlparse
import requests
#from urllib import urlretrieve
import os
import sys
import re

REGEX = [
    {"domain": "example.com", "find": re.compile("thumbs\/.*thumbs_(www-[^.]+\.jpg)(\.pagespeed\.ic\..+\.jpg)?", re.I), "replace":r"\1"},
    {"domain": "example.org", "find": re.compile("thumb_", re.I), "replace":""},

    ]

join = os.path.join
urljoin = urlparse.urljoin
urlsplit = urlparse.urlsplit

def main(urls, out_folder="/test/"):
    """Downloads all the images at 'url' to /test/"""
    for url in urls:
        if not url.startswith('http'):
            continue
        soup = get_page(url)
        srcs = find_images(soup)
        for src in [x for x in srcs if x]:
            imagepath = urljoin(url, src)
            # do regex replacement
            image = process_url(imagepath)
            if not image:
                continue
            print imagepath
            print image
            # get the filename from the updated url
            imagename = name_from_url(image)
            filename = join(out_folder, imagename)
            if os.path.isfile(filename): # no clobber
                continue
            save_image_to_disk(image, filename)


def name_from_url(url):
    '''Return only the filename from a url'''
    return url.split('/')[-1]

def get_page(url):
    '''Given a url, fetch and return the page'''
    page = requests.get(url).text
    return bs(page)

def find_images(soup):
    '''Return a list of <img>s found in soup'''
    return [image['src'] for image in soup.findAll("img") if image['src']]

def save_image_to_disk(image, filename):
    response = requests.get(image, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
    else:
        print response.status_code, image
    del response

def process_url(url):
    '''Return url after doing a regex replacement'''
    for site in REGEX: # loop over the list of regex
        if re.search(site['domain'], url): # test our url against the defined domain
            # if we find a match, run the regex replacement and return
            return site['find'].sub(site['replace'], url)

def urls_from_file(fname):
    return open(fname).read().split('\n')

def _usage():
    print """usage:
        python {0} (fileofurls or url[s]) [outpath]

        python {0} http://example.com ./dest
        python {0} http://example.com,http://otherexample.com ./dest
        python {0} urls.txt ./dest
        """.format(sys.argv[1])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        _usage()
        sys.exit(-1)
    urls = [sys.argv[-1]]
    out_folder = "/test/"
    if not urls[0].lower().startswith("http"):
        out_folder = sys.argv[-1]
        urls = sys.argv[-2].split(',')
    if not urls[0].lower().startswith("http"):
        urls = urls_from_file(urls[0])

    main(urls, out_folder)