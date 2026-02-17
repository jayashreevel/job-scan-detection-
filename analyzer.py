import whois
from datetime import datetime

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
    try:
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        w = whois.whois(domain)
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]

        age_days = (datetime.now() - creation).days
        return age_days < 365
    except:
        return True
