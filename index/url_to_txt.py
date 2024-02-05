
import urllib.request
from bs4 import BeautifulSoup


def Web2Text(url, outname):
    # Header for the http request
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent, }

    # Request and read the html from the given url
    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    data = response.read()  # HTML data of the web page's source

    # Clean html
    raw = BeautifulSoup(data).get_text()
    print(raw)

    with open(outname, 'w',  encoding="utf-8") as outf:
        outf.writelines(raw)


with open("../data/urls.txt") as file:
    for url in file:
        curr_url = url.rstrip()
        out_file = "../data/txt_files/%s.txt" % (curr_url)
        print(out_file)
        Web2Text(curr_url, "../data/txt_files/visibility_gurus.txt")
