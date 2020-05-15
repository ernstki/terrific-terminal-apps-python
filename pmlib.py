import requests
import lxml.html

from urllib.parse import quote as urlquote


NCBI_BASE_URL = 'https://www.ncbi.nlm.nih.gov'
NCBI_SEARCH_PATH = 'pubmed/?term='
NCBI_DEFAULT_SEARCH_TERM = 'notch'
NCBI_SEARCH_RESULT_TITLE_A_XPATH = '//p[@class="title"]/a'


def pubmed_query(terms):
    if terms is None:
        terms = []

    results = [];

    query_url = NCBI_BASE_URL + '/' + NCBI_SEARCH_PATH \
              + urlquote(' '.join(terms))

    with requests.Session() as s:
        response = s.get(query_url)
        assert response.ok
        html = lxml.html.fromstring(response.content)
        anchors = html.xpath(NCBI_SEARCH_RESULT_TITLE_A_XPATH)

    for anchor in anchors:
        results.append([
            NCBI_BASE_URL + anchor.attrib['href'],
            anchor.text_content()
        ])

    return results
