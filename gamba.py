import concurrent.futures
import requests
from bs4 import BeautifulSoup
import os

TIMEOUT = 8
MAX_WORKERS = 120

SOURCES = [
    # HTTP / HTTPS
    ("http", "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/master/http.txt"),
    ("http", "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/master/https.txt"),
    ("http", "https://proxyspace.pro/http.txt"),
    ("http", "https://proxyspace.pro/https.txt"),
    ("http", "https://vakhov.github.io/fresh-proxy-list/http.txt"),
    ("http", "https://vakhov.github.io/fresh-proxy-list/https.txt"),
    ("http", "https://www.free-proxy-list.net/anonymous-proxy.txt"),
    ("http", "https://www.free-proxy-list.net/uk-proxy.txt"),
    ("http", "https://www.free-proxy-list.net/us-proxy.txt"),
    ("http", "https://raw.githubusercontent.com/iplocate/free-proxy-list/main/protocols/http.txt"),
    ("http", "https://raw.githubusercontent.com/iplocate/free-proxy-list/main/protocols/https.txt"),
    ("http", "https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/http.txt"),
    ("http", "https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/https.txt"),
    ("http", "https://www.proxyrack.com/free-proxy-list?format=txt"),
    ("http", "https://free-proxy-list.net/?page=1&uptime=100&sort=uptime&order=desc&type=http"),
    ("http", "https://geonode.com/free-proxy-list?protocol=http#list"),
    ("http", "https://proxylist.download/api/proxylist.txt?type=http"),
    ("http", "https://raw.githubusercontent.com/jundymek/free-proxy/master/free-proxy.txt"),
    ("http", "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"),
    ("http", "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt"),
    ("http", "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt"),
    ("http", "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt"),
    ("http", "https://raw.githubusercontent.com/hproxy-com/free-proxy-list/refs/heads/main/http.txt"),
    ("http", "https://raw.githubusercontent.com/hproxy-com/free-proxy-list/refs/heads/main/https.txt"),
    ("http", "https://cdn.jsdelivr.net/gh/proxyscrape/free-proxy-list@main/proxies/protocols/http/data.txt"),
    ("http", "https://cdn.jsdelivr.net/gh/proxyscrape/free-proxy-list@main/proxies/protocols/https/data.txt"),
    ("http", "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/http.txt"),
    ("http", "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/https.txt"),
    ("http", "https://raw.githubusercontent.com/VPSLabCloud/VPSLab-Free-Proxy-List/main/http_all.txt"),
    ("http", "https://raw.githubusercontent.com/RioMMO/ProxyFree/refs/heads/main/HTTP.txt"),
    ("http", "https://raw.githubusercontent.com/zloi-user/hideip.me/master/http.txt"),
    ("http", "https://raw.githubusercontent.com/zloi-user/hideip.me/master/https.txt"),
    ("http", "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"),
    ("http", "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"),
    ("http", "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt"),
    ("http", "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/http/data.txt"),
    ("http", "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt"),

    # SOCKS4
    ("socks4", "https://proxyspace.pro/socks4.txt"),
    ("socks4", "https://vakhov.github.io/fresh-proxy-list/socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/master/socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/iplocate/free-proxy-list/main/protocols/socks4.txt"),
    ("socks4", "https://proxylist.download/api/proxylist.txt?type=socks4"),
    ("socks4", "https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/hproxy-com/free-proxy-list/refs/heads/main/socks4.txt"),
    ("socks4", "https://cdn.jsdelivr.net/gh/proxyscrape/free-proxy-list@main/proxies/protocols/socks4/data.txt"),
    ("socks4", "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/VPSLabCloud/VPSLab-Free-Proxy-List/main/socks4_all.txt"),
    ("socks4", "https://raw.githubusercontent.com/RioMMO/ProxyFree/refs/heads/main/SOCKS4.txt"),
    ("socks4", "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt"),
    ("socks4", "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt"),
    ("socks4", "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks4_proxies.txt"),

    # SOCKS5
    ("socks5", "https://proxyspace.pro/socks5.txt"),
    ("socks5", "https://vakhov.github.io/fresh-proxy-list/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/master/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/iplocate/free-proxy-list/main/protocols/socks5.txt"),
    ("socks5", "https://proxylist.download/api/proxylist.txt?type=socks5"),
    ("socks5", "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"),
    ("socks5", "https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/hproxy-com/free-proxy-list/refs/heads/main/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/VPSLabCloud/VPSLab-Free-Proxy-List/main/socks5_all.txt"),
    ("socks5", "https://raw.githubusercontent.com/RioMMO/ProxyFree/refs/heads/main/SOCKS5.txt"),
    ("socks5", "https://cdn.jsdelivr.net/gh/proxyscrape/free-proxy-list@main/proxies/protocols/socks5/data.txt"),
    ("socks5", "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt"),
    ("socks5", "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks5/data.txt"),
    ("socks5", "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks5_proxies.txt")
]

def fetch_source(p_type, url):
    found = set()

    try:
        r = requests.get(url, timeout=TIMEOUT)

        if r.status_code != 200:
            return p_type, found

        text = r.text.replace("\ufeff", "")

        if "<" in text and ">" in text:
            text = BeautifulSoup(text, "lxml").get_text()

        for line in text.splitlines():
            line = line.strip()

            if line and ":" in line:
                found.add(line)

    except Exception:
        pass

    return p_type, found


def scrape_proxies():
    proxies = {
        "http": set(),
        "socks4": set(),
        "socks5": set()
    }

    print(f"[+] Scraping {len(SOURCES)} sources...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(fetch_source, p_type, url)
            for p_type, url in SOURCES
        ]

        for future in concurrent.futures.as_completed(futures):
            p_type, found = future.result()
            proxies[p_type].update(found)

    return proxies


def save_proxies(proxies):
    os.makedirs("scraped", exist_ok=True)

    for p_type, proxy_set in proxies.items():
        path = f"scraped/{p_type}_proxies.txt"

        with open(path, "w", encoding="utf-8") as f:
            for proxy in sorted(proxy_set):
                f.write(proxy + "\n")

        print(f"[✓] Saved {len(proxy_set)} {p_type} proxies -> {path}")


if __name__ == "__main__":
    proxies = scrape_proxies()

    print(
        f"[✓] Scraped "
        f"{len(proxies['http'])} HTTP | "
        f"{len(proxies['socks4'])} SOCKS4 | "
        f"{len(proxies['socks5'])} SOCKS5"
    )

    save_proxies(proxies)
