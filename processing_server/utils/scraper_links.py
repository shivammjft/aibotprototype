# scraper.py
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

EXCLUDE_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',".mp3",".mp4"}

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Request to {url} failed with status code {response.status}")
                return None
    except Exception as e:
        print(f"Request to {url} failed: {e}")
        return None

def is_webpage(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    return not any(path.endswith(ext) for ext in EXCLUDE_EXTENSIONS)

async def extract_links(session, url, domain, depth=2, max_links=500):
    links = set()
    queue = [(url, 0)]

    while queue and len(links) < max_links:
        current_url, current_depth = queue.pop(0)
        if current_depth > depth:
            continue

        html = await fetch(session, current_url)
        if not html:
            continue

        soup = BeautifulSoup(html, 'html.parser')
        page_links = [urljoin(current_url, a.get('href')) for a in soup.find_all('a', href=True)]
        for link in page_links:
            if link not in links and urlparse(link).netloc == domain and is_webpage(link):
                links.add(link)
                queue.append((link, current_depth + 1))
                print(f"Found link: {link}")

    return list(links)

async def get_links(url):
    domain = urlparse(url).netloc
    async with aiohttp.ClientSession() as session:
        links = await extract_links(session, url, domain)
    return links
