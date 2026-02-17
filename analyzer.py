from datetime import datetime

# Try importing whois safely
try:
    import whois
except ImportError:
    whois = None

# Weighted scam keywords
keyword_weights = {
    "registration fee": 5,
    "processing fee": 5,
    "telegram": 4,
    "whatsapp": 4,
    "earn per day": 3,
    "easy money": 3,
    "work from home": 2,
    "no experience": 2
}

def check_keywords(text):
    score = 0
    matched = []

    for word, weight in keyword_weights.items():
        if word in text.lower():
            score += weight
            matched.append(word)

    return score, matched


def domain_age_check(url):
    """
    Returns True if domain is risky (new or unknown)
    Returns False if domain looks safe
    """
    # If whois not available in cloud, mark as safe fallback
    if whois is None:
        return False

    try:
        domain = url.replace("http://", "").replace("https://", "").split("/")[0]
        w = whois.whois(domain)

        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]

        if creation is None:
            return True

        age_days = (datetime.now() - creation).days

        # Domain younger than 1 year → risky
        return age_days < 365

    except Exception:
        # Any error → do NOT crash app
        return False
