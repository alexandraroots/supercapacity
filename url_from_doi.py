from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def get_paper_url_from_doi(url):
    url = "https://sci-hub.ru" + url
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()
    soup = BeautifulSoup(html_page, 'html.parser')
    div = soup.find(id="buttons")
    ref = div.button['onclick']
    print(ref)
    ref = ref.split("='")[1].split("?")[0]
    if ref[1] == "/":  # Not on sci-hub <- основано на целых 3 ссылках
        return "https:" + ref
    else: # on sci-hub
        return "https://sci-hub.ru" + ref


if __name__ == "__main__":
    url_1 = "https://doi.org/10.1039/D0RA07620A"
    url_2 = "https://doi.org/10.1039/C4TA02390K"
    url_3 = "https://doi.org/10.1016/j.vaa.2017.02.002"
    url_4 = "https://doi.org/10.1186/s11671-018-2819-4"
    url_5 = "https://doi.org/10.1134/S0036023621120160"
    urls = [url_1, url_2, url_3, url_4, url_5]
    # urls = [url_3]

    for ur in urls:
        result = get_paper_url_from_doi(ur)
        print(result)
