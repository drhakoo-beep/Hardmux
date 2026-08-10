import socket
import re
import datetime

try:
    import requests
except ImportError:
    requests = None

try:
    import whois
except ImportError:
    whois = None

try:
    import dns.resolver
except ImportError:
    dns = None

SITES = {
    "GitHub": "https://github.com/{}",
    "Twitter/X": "https://x.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Telegram": "https://t.me/{}",
    "Medium": "https://medium.com/@{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Facebook": "https://www.facebook.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Vimeo": "https://vimeo.com/{}",
    "Flickr": "https://www.flickr.com/people/{}",
    "Behance": "https://www.behance.net/{}",
    "Dribbble": "https://dribbble.com/{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "Keybase": "https://keybase.io/{}",
    "Patreon": "https://www.patreon.com/{}",
    "Codepen": "https://codepen.io/{}",
    "Replit": "https://replit.com/@{}",
    "NPM": "https://www.npmjs.com/~{}",
    "PyPI": "https://pypi.org/user/{}",
    "Docker Hub": "https://hub.docker.com/u/{}",
    "SourceForge": "https://sourceforge.net/u/{}/profile",
    "Kaggle": "https://www.kaggle.com/{}",
}

COUNTRY_CODES = {
    "1": "US/CA", "7": "RU/KZ", "20": "EG", "27": "ZA", "30": "GR",
    "31": "NL", "32": "BE", "33": "FR", "34": "ES", "36": "HU",
    "39": "IT", "40": "RO", "41": "CH", "43": "AT", "44": "GB",
    "45": "DK", "46": "SE", "47": "NO", "48": "PL", "49": "DE",
    "51": "PE", "52": "MX", "54": "AR", "55": "BR", "56": "CL",
    "57": "CO", "58": "VE", "60": "MY", "61": "AU", "62": "ID",
    "63": "PH", "64": "NZ", "65": "SG", "66": "TH", "81": "JP",
    "82": "KR", "84": "VN", "86": "CN", "90": "TR", "91": "IN",
    "92": "PK", "93": "AF", "94": "LK", "95": "MM", "98": "IR",
    "212": "MA", "213": "DZ", "216": "TN", "218": "LY", "220": "GM",
    "234": "NG", "254": "KE", "351": "PT", "352": "LU", "353": "IE",
    "358": "FI", "370": "LT", "371": "LV", "372": "EE", "380": "UA",
    "420": "CZ", "421": "SK", "852": "HK", "886": "TW", "961": "LB",
    "962": "JO", "963": "SY", "964": "IQ", "965": "KW", "966": "SA",
    "971": "AE", "972": "IL", "973": "BH", "974": "QA", "975": "BT",
}


def username_search(username):
    if requests is None:
        return "requests modulu kurulu degil: pip install requests"
    results = []
    for site, url_fmt in SITES.items():
        url = url_fmt.format(username)
        try:
            r = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            found = r.status_code == 200
        except Exception:
            found = False
        results.append("[{}] {}: {}".format("+" if found else "-", site, url))
    return "\n".join(results)


def social_link_generator(username):
    lines = [url_fmt.format(username) + "  (" + site + ")" for site, url_fmt in SITES.items()]
    return "\n".join(lines)


def whois_lookup(domain):
    if whois is None:
        return "python-whois modulu kurulu degil: pip install python-whois"
    try:
        w = whois.whois(domain)
        return str(w)
    except Exception as e:
        return "Hata: {}".format(e)


def domain_age(domain):
    if whois is None:
        return "python-whois modulu kurulu degil"
    try:
        w = whois.whois(domain)
        created = w.creation_date
        if isinstance(created, list):
            created = created[0]
        if created is None:
            return "Olusturma tarihi bulunamadi"
        if isinstance(created, str):
            return "Olusturma tarihi (ham): {}".format(created)
        age = datetime.datetime.now() - created.replace(tzinfo=None)
        return "Olusturma Tarihi: {}\nYas: {} gun (~{:.1f} yil)".format(created, age.days, age.days / 365.25)
    except Exception as e:
        return "Hata: {}".format(e)


def dns_lookup(domain):
    output = []
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]
    if dns is not None:
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(domain, rtype, lifetime=5)
                for rdata in answers:
                    output.append("{}: {}".format(rtype, rdata.to_text()))
            except Exception:
                continue
    else:
        try:
            ip = socket.gethostbyname(domain)
            output.append("A: {}".format(ip))
        except Exception as e:
            output.append("Hata: {}".format(e))
    return "\n".join(output) if output else "Kayit bulunamadi"


def ip_lookup(ip_or_host):
    try:
        ip = socket.gethostbyname(ip_or_host)
    except Exception as e:
        return "Cozumleme hatasi: {}".format(e)
    if requests is None:
        return "IP: {}\nrequests modulu kurulu degil, detay alinamadi".format(ip)
    try:
        r = requests.get("https://ipinfo.io/{}/json".format(ip), timeout=5)
        data = r.json()
        lines = ["{}: {}".format(k, v) for k, v in data.items()]
        return "\n".join(lines)
    except Exception as e:
        return "IP: {}\nSorgu hatasi: {}".format(ip, e)


def email_format_analysis(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    valid = re.match(pattern, email) is not None
    if not valid:
        return "Gecersiz email formati"
    local, domain = email.split("@")
    result = []
    result.append("Local part: {}".format(local))
    result.append("Domain: {}".format(domain))
    try:
        ip = socket.gethostbyname(domain)
        result.append("Domain IP: {}".format(ip))
    except Exception:
        result.append("Domain cozumlenemedi")
    try:
        mx_records = []
        if dns is not None:
            answers = dns.resolver.resolve(domain, "MX", lifetime=5)
            for rdata in answers:
                mx_records.append(rdata.to_text())
        result.append("MX Records: {}".format(", ".join(mx_records) if mx_records else "yok/none"))
    except Exception:
        result.append("MX kayitlari alinamadi")
    return "\n".join(result)


def phone_number_analysis(number):
    cleaned = re.sub(r"[^0-9+]", "", number)
    if not cleaned.startswith("+"):
        return "Uluslararasi format icin basina + koyun (orn +905551234567)"
    digits = cleaned[1:]
    match_code = None
    for length in (3, 2, 1):
        prefix = digits[:length]
        if prefix in COUNTRY_CODES:
            match_code = prefix
            break
    lines = ["Girilen: {}".format(cleaned), "Rakam sayisi: {}".format(len(digits))]
    if match_code:
        lines.append("Ulke kodu: +{} ({})".format(match_code, COUNTRY_CODES[match_code]))
    else:
        lines.append("Ulke kodu tanimlanamadi")
    return "\n".join(lines)


def google_dork_generator(domain):
    dorks = [
        "site:{} filetype:pdf".format(domain),
        "site:{} filetype:xlsx".format(domain),
        "site:{} filetype:docx".format(domain),
        "site:{} inurl:admin".format(domain),
        "site:{} inurl:login".format(domain),
        "site:{} intitle:\"index of\"".format(domain),
        "site:{} ext:sql".format(domain),
        "site:{} ext:env".format(domain),
        "site:{} inurl:config".format(domain),
        "site:{} intext:password".format(domain),
        "site:pastebin.com \"{}\"".format(domain),
        "site:github.com \"{}\"".format(domain),
        "site:linkedin.com/in \"{}\"".format(domain),
    ]
    return "\n".join(dorks)
