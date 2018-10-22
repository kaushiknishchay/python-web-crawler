from bs4 import BeautifulSoup
import requests
import sys
import re
from urlparse import urlparse

matched_links = 0
total_links = 0


def get_keyword(keyword, source):
    keyword_regex = r".{10}" + keyword + ".{10}"
    matches = re.findall(keyword_regex, source,
                         re.MULTILINE | re.IGNORECASE | re.DOTALL)
    if(len(matches) > 0):
        return "".join(matches[0])
    else:
        return None


def get_page_source(page_url):
    r = requests.get(page_url)
    data = r.text
    return data


def get_content(data):
    data = re.sub(r'<style>.*?[\s]*[\w\W]*[\d]*<\/style>', '', data)
    data = re.sub(r'<script>.*?[\s]*[\w\W]*[\d]*<\/script>', '', data)
    data = re.sub(r'<\/?[^>]*>', '', data)
    return data


def get_page_links(page_url):
    global matched_links
    # parse url
    parse_url = urlparse(page_url)
    # create base url
    base_url = parse_url.scheme + '://' + parse_url.netloc
    # get page source
    page_source = get_page_source(page_url)
    # make page source soup
    soup = BeautifulSoup(page_source, features="html.parser")

    page_keyword = get_keyword(keyword, get_content(page_source))

    if (not page_keyword == None):
        matched_links += 1
        print page_url + " : " + page_keyword.strip()

    for link in soup.find_all('a'):
        href = link.get('href')
        if(not href == None and not href.startswith('#')):
            if ("http://" in href or "https://" in href):
                if (href.startswith(page_url) and href not in to_explore):
                    to_explore.append(href)
            elif (href.startswith('/')):
                abs_href = base_url + href
                if (abs_href.startswith(page_url) and abs_href not in to_explore):
                    to_explore.append(abs_href)
    return to_explore


if __name__ == "__main__":
    if(len(sys.argv) <= 2):
        url = raw_input("Enter a website url: ")
        keyword = raw_input("Enter keyword: ")
    else:
        url = str(sys.argv[1])
        keyword = str(sys.argv[2])

    # track links to follow
    to_explore = [url]

    for link in to_explore:
        get_page_links(link)
        total_links += 1

    print "Total Links Crawled: ", total_links
    print "Found on pages: ", matched_links
