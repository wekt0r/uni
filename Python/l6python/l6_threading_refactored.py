import re
import urllib.request

import threading
import queue
from bs4 import BeautifulSoup
from time import time

HTML_URL_REGEX = re.compile(r'<a.*?href=[\'|\"](.*?)[\'|\"].*?>', re.IGNORECASE)
PYTHON_REGEX = re.compile(r'python', re.IGNORECASE)

def impose_function_on_website_and_subsites(action, main_url, depth=5):
    with urllib.request.urlopen(main_url) as website:
        website_body = website.read().decode('utf-8','ignore')
    website_checker = WebsiteChecker()

    return _impose_function_on_website_and_subsites(action, main_url, website_body, depth, website_checker)

class WebsiteChecker:
    def __init__(self):
        self.already_visited = []
    def get_website(self, url, q):
        if url not in self.already_visited:
            self.already_visited.append(url)
            try:
                with urllib.request.urlopen(url) as website:
                    website_body = website.read().decode('utf-8','ignore')
                q.put((url, website_body))
            except:
                pass
        else:
            pass

def _get_website(url):
    with urllib.request.urlopen(url) as website:
        return website.read().decode('utf-8','ignore')

def _impose_function_on_website_and_subsites(action, main_url, website_body, depth, website_checker):
    if depth > 0:
        #try:
            yield action(website_body)
            print("how many times im here?")
            q = queue.Queue()
            urls = [url if url.startswith("http") else main_url + url for url in re.findall(HTML_URL_REGEX, website_body) ]
            threads = [threading.Thread(target=website_checker.get_website, args=(url,q)) for url in urls]
            for thread in threads:
                print("am i here?")
                thread.start()
            for thread in threads:
                thread.join()

            while q:
                url,body = q.get()
                yield from _impose_function_on_website_and_subsites(action, url, body, depth-1, website_checker)
            #website_reader.close()
            #website_reader.join()

        # except urllib.error.HTTPError:
        #     yield "Connection Error on {}".format(main_url)
        # except:
        #     yield "Processing Error on {}".format(main_url)

def get_all_python_sentences(html_page):
    sentences = BeautifulSoup(html_page, 'html.parser').get_text().split(".")
    return [sentence for sentence in sentences if re.search(PYTHON_REGEX, sentence)]

#some test
if __name__ == "__main__":
    begin = time()
    print("---")
    for ls in impose_function_on_website_and_subsites(get_all_python_sentences, "https://www.ii.uni.wroc.pl/~marcinm/dyd/python/", 2):
        if isinstance(ls, list):
            print("\n*".join(ls))
            #print(ls)
        else:
            print(ls)
            print("---")
    print("it took {}".format(time() - begin))
