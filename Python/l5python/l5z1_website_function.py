import re
import urllib.request
from bs4 import BeautifulSoup

HTML_URL_REGEX = re.compile(r'<a.*?href=[\'|\"](.*?)[\'|\"].*?>', re.IGNORECASE)
PYTHON_REGEX = re.compile(r'python', re.IGNORECASE)

def impose_function_on_website_and_subsites(action, main_url, depth=5):
    return _impose_function_on_website_and_subsites(action, main_url, depth, set())

def _impose_function_on_website_and_subsites(action, main_url, depth, already_visited_static=set()):
    if depth > 0:
        try:
            with urllib.request.urlopen(main_url) as website:
                website_body = website.read().decode('utf-8','ignore')

            yield action(website_body)

            for url in re.findall(HTML_URL_REGEX, website_body):
                if not url.startswith("http"):
                    url = main_url + url
                if url not in already_visited_static:
                    already_visited_static.add(url)
                    yield from _impose_function_on_website_and_subsites(action, url, depth-1)

        except urllib.error.HTTPError:
            yield "Connection Error on {}".format(main_url)
        except:
            yield "Processing Error on {}".format(main_url)

def get_all_python_sentences(html_page):
    sentences = BeautifulSoup(html_page, 'html.parser').get_text().split(".")
    return [sentence for sentence in sentences if re.search(PYTHON_REGEX, sentence)]

#some test
print("---")
for ls in impose_function_on_website_and_subsites(get_all_python_sentences, "https://www.ii.uni.wroc.pl/~marcinm/dyd/python/", 2):
    if isinstance(ls, list):
        print("*\n".join(ls))
        #print(ls)
    else:
        print(ls)
    print("---")
