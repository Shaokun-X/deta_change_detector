import requests
import logging
from typing import Optional
from fake_useragent import UserAgent
from lxml import html

logger = logging.getLogger(__name__)

ua = UserAgent()

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "User-Agent": ua.chrome
}

def scrape(url: str, xpath: str) -> Optional[str]:
    has_falied = False
    elements = []
    try:
        response = requests.get(url, headers=HEADERS)
        content = html.fromstring(response.text)
        elements = content.xpath(xpath)
    except:
        has_falied = True
    if not elements or not isinstance(elements[0], str):
        has_falied = True
    if has_falied:
        logger.info("Failed to extract text from the response with given xpath.\n%s\n%s", url, xpath)
        return None
    return elements[0].strip()