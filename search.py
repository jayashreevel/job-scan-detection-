from duckduckgo_search import DDGS

def google_search(text):
    links = []
    with DDGS() as ddgs:
        results = ddgs.text(text, max_results=5)
        for r in results:
            links.append(r["href"])
    return links
