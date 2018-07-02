import re
import urllib.request
from multiprocessing.dummy import Pool

from bs4 import BeautifulSoup
from time import time

HTML_URL_REGEX = re.compile(r'<a.*?href=[\'|\"](.*?)[\'|\"].*?>', re.IGNORECASE)
PYTHON_REGEX = re.compile(r'python', re.IGNORECASE)
ALREADY_VISITED_STATIC = []

def impose_function_on_website_and_subsites(action, main_url, depth=5):
    return _impose_function_on_website_and_subsites(action, main_url, depth)

def _inspect(url, action, main_url, depth):
    if not url.startswith("http"):
        url = main_url + url
    if url not in ALREADY_VISITED_STATIC:
        ALREADY_VISITED_STATIC.append(url)
        yield from _impose_function_on_website_and_subsites(action, url, depth-1)

def _get_website(main_url):
    with urllib.request.urlopen(main_url) as website:
        return website.read().decode('utf-8','ignore')

def _impose_function_on_website_and_subsites(action, main_url, depth):
    if depth > 0:
        try:
            # reader = Pool()
            # read = reader.apply(_get_website, (main_url,))
            # reader.close()
            # reader.join()
            # website_body = read
            "^ works slower than this v"
            with urllib.request.urlopen(main_url) as website:
                website_body = website.read().decode('utf-8','ignore')

            yield action(website_body)

            pool = Pool(8)
            results = pool.starmap(_inspect, [(url, action, main_url, depth) for url in re.findall(HTML_URL_REGEX, website_body)])
            pool.close()
            pool.join()

            for result in results:
                yield from result

        except urllib.error.HTTPError:
            yield "Connection Error on {}".format(main_url)
        except:
            yield "Processing Error on {}".format(main_url)

def get_all_python_sentences(html_page):
    sentences = BeautifulSoup(html_page, 'html.parser').get_text().split(".")
    return "".join([sentence for sentence in sentences if re.search(PYTHON_REGEX, sentence)])

#some test
t0 = time()
counter = 0
for element in impose_function_on_website_and_subsites(get_all_python_sentences, "https://www.ii.uni.wroc.pl/~marcinm/dyd/python/", 2):
    counter += 1
    print(element)

print(counter)
print("multiprocessing version took {}".format(time() - t0))
