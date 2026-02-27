import os
import logging
import requests
import lxml.html

from urllib.parse import quote as urlquote

NCBI_BASE_URL = 'https://www.ncbi.nlm.nih.gov'
NCBI_SEARCH_PATH = 'pubmed/?term='
NCBI_DEFAULT_SEARCH_TERM = 'notch'
NCBI_SEARCH_RESULT_TITLE_A_XPATH = '//a[@class="docsum-title"]'

logger = logging.getLogger(__name__)
fmt = '[%(levelname)s:%(name)s] %(asctime)s - %(message)s'

if os.getenv('DEBUG') or os.getenv('PMLIB_DEBUG'):
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

def pubmed_query(terms):
    if terms is None:
        terms = []

    results = [];

    query_url = NCBI_BASE_URL + '/' + NCBI_SEARCH_PATH \
              + urlquote(' '.join(terms))

    with requests.Session() as s:
        logger.debug(f"Sending query '{query_url}'…")
        response = s.get(query_url)
        logger.debug(f"Got response: {response.status_code}")
        assert response.ok
        html = lxml.html.fromstring(response.content)
        anchors = html.xpath(NCBI_SEARCH_RESULT_TITLE_A_XPATH)
        logger.debug(f"Found {len(anchors)} matching anchors in document")

    for anchor in anchors:
        results.append([
            NCBI_BASE_URL + anchor.attrib['href'],
            anchor.text_content().strip()
        ])

    return results
