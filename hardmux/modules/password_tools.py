import re
import secrets
import string
import math

COMMON_PASSWORDS = {
    "123456", "password", "12345678", "qwerty", "123456789", "12345",
    "1234", "111111", "1234567", "dragon", "123123", "baseball",
    "abc123", "football", "monkey", "letmein", "shadow", "master",
    "666666", "qwertyuiop", "123321", "mustang", "1234567890",
    "michael", "654321", "superman", "1qaz2wsx", "7777777",
    "121212", "000000", "qazwsx", "trustno1", "iloveyou",
}

DICEWARE_WORDS = [
    "kaya", "nehir", "orman", "gunes", "ay", "yildiz", "deniz", "dag",
    "kurt", "kartal", "aslan", "kaplan", "ates", "buz", "ruzgar", "toprak",
    "demir", "altin", "gumus", "bakir", "kalkan", "kilic", "ok", "yay",
    "kale", "koprk", "yol", "kapi", "pencere", "duvar", "cati", "bahce",
]


def check_strength(password, labels):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("En az 8 karakter olmali / Should be at least 8 characters")

    if len(password) >= 12:
        score += 1

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Kucuk harf eksik / Missing lowercase")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Buyuk harf eksik / Missing uppercase")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Rakam eksik / Missing digit")

    if re.search(r"[^a-zA-Z0-9]", password):
        score += 1
    else:
        feedback.append("Ozel karakter eksik / Missing special character")

    if password.lower() in COMMON_PASSWORDS:
        score = 0
        feedback.append("Bilinen zayif parola / Known weak password")

    if score <= 2:
        level = labels["weak"]
    elif score <= 4:
        level = labels["medium"]
    elif score <= 5:
        level = labels["strong"]
    else:
        level = labels["very_strong"]

    lines = ["Skor: {}/6".format(score), "Seviye: {}".format(level)]
    if feedback:
        lines.append("Notlar:")
        lines.extend(["  - " + f for f in feedback])
    return "\n".join(lines)


def common_password_check(password):
    if password.lower() in COMMON_PASSWORDS:
        return "UYARI: Bu parola bilinen yaygin parolalar listesinde bulunuyor."
    return "Bu parola yerel yaygin-parola listesinde bulunamadi (guvenli anlamina gelmez)."


def password_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"[0-9]", password):
        charset += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        charset += 32
    if charset == 0 or len(password) == 0:
        return "Parola girilmedi"
    entropy = len(password) * math.log2(charset)
    return "Karakter uzayi: {}\nUzunluk: {}\nEntropi: {:.1f} bit".format(charset, len(password), entropy)


def generate_password(length=16, use_symbols=True):
    try:
        length = int(length)
    except Exception:
        length = 16
    length = max(4, min(length, 128))
    alphabet = string.ascii_letters + string.digits
    if use_symbols:
        alphabet += "!@#$%^&*()-_=+[]{}"
    while True:
        pwd = "".join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in pwd) and any(c.isupper() for c in pwd)
                and any(c.isdigit() for c in pwd)):
            return pwd


def generate_passphrase(word_count):
    try:
        word_count = int(word_count)
    except Exception:
        word_count = 5
    word_count = max(3, min(word_count, 12))
    words = [secrets.choice(DICEWARE_WORDS) for _ in range(word_count)]
    return "-".join(words)


def generate_pin(length):
    try:
        length = int(length)
    except Exception:
        length = 6
    length = max(4, min(length, 12))
    return "".join(secrets.choice(string.digits) for _ in range(length))


def generate_wordlist(base_words, max_combinations=200):
    words = [w.strip() for w in base_words.split(",") if w.strip()]
    if not words:
        return "Kelime girilmedi"
    suffixes = ["", "1", "12", "123", "!", "2024", "2025", "2026", "01", "007"]
    prefixes = ["", "!"]
    results = set()
    for w in words:
        variants = {w, w.lower(), w.upper(), w.capitalize()}
        for v in variants:
            for p in prefixes:
                for s in suffixes:
                    results.add(p + v + s)
                    if len(results) >= max_combinations:
                        break
    result_list = sorted(results)[:max_combinations]
    return "\n".join(result_list)
