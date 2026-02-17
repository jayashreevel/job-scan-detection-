# Safe import for cloud environments
try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None


def google_search(text):
    """
    Returns list of related links.
    If DuckDuckGo blocks or library missing,
    returns empty list without crashing.
    """
    links = []

    if DDGS is None:
        return links

    try:
        with DDGS() as ddgs:
            results = ddgs.text(text, max_results=5)
            for r in results:
                link = r.get("href")
                if link:
                    links.append(link)
    except Exception:
        pass

    return links
