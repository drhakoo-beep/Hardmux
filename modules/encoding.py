import base64
import binascii
import urllib.parse
import html
import uuid
import secrets
import json

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b64_encode(text):
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def b64_decode(text):
    try:
        return base64.b64decode(text.encode("utf-8")).decode("utf-8", errors="replace")
    except Exception as e:
        return "Hata: {}".format(e)


def b32_encode(text):
    return base64.b32encode(text.encode("utf-8")).decode("utf-8")


def b32_decode(text):
    try:
        return base64.b32decode(text.encode("utf-8")).decode("utf-8", errors="replace")
    except Exception as e:
        return "Hata: {}".format(e)


def b85_encode(text):
    return base64.a85encode(text.encode("utf-8")).decode("utf-8")


def b85_decode(text):
    try:
        return base64.a85decode(text.encode("utf-8")).decode("utf-8", errors="replace")
    except Exception as e:
        return "Hata: {}".format(e)


def base58_encode(text):
    data = text.encode("utf-8")
    num = int.from_bytes(data, "big")
    encoded = ""
    while num > 0:
        num, rem = divmod(num, 58)
        encoded = BASE58_ALPHABET[rem] + encoded
    n_pad = len(data) - len(data.lstrip(b"\x00"))
    return "1" * n_pad + encoded


def base58_decode(text):
    try:
        num = 0
        for ch in text:
            num = num * 58 + BASE58_ALPHABET.index(ch)
        combined = num.to_bytes((num.bit_length() + 7) // 8, "big")
        n_pad = len(text) - len(text.lstrip("1"))
        result = b"\x00" * n_pad + combined
        return result.decode("utf-8", errors="replace")
    except Exception as e:
        return "Hata: {}".format(e)


def hex_encode(text):
    return text.encode("utf-8").hex()


def hex_decode(text):
    try:
        return bytes.fromhex(text.strip()).decode("utf-8", errors="replace")
    except Exception as e:
        return "Hata: {}".format(e)


def binary_encode(text):
    return " ".join(format(b, "08b") for b in text.encode("utf-8"))


def binary_decode(text):
    try:
        chunks = text.split()
        data = bytes(int(c, 2) for c in chunks)
        return data.decode("utf-8", errors="replace")
    except Exception as e:
        return "Hata: {}".format(e)


def url_encode(text):
    return urllib.parse.quote(text)


def url_decode(text):
    return urllib.parse.unquote(text)


def html_encode(text):
    return html.escape(text)


def html_decode(text):
    return html.unescape(text)


def unicode_escape_encode(text):
    return text.encode("unicode_escape").decode("ascii")


def unicode_escape_decode(text):
    try:
        return text.encode("ascii").decode("unicode_escape")
    except Exception as e:
        return "Hata: {}".format(e)


def punycode_encode(text):
    try:
        return text.encode("punycode").decode("ascii")
    except Exception as e:
        return "Hata: {}".format(e)


def punycode_decode(text):
    try:
        return text.encode("ascii").decode("punycode")
    except Exception as e:
        return "Hata: {}".format(e)


def uuid_generate(_unused=None):
    return str(uuid.uuid4())


def random_token(length):
    try:
        length = int(length)
    except Exception:
        length = 32
    length = max(4, min(length, 256))
    return secrets.token_hex(length // 2)


def random_urlsafe_token(length):
    try:
        length = int(length)
    except Exception:
        length = 32
    length = max(4, min(length, 256))
    return secrets.token_urlsafe(length)


def jwt_decode(token):
    try:
        parts = token.split(".")
        if len(parts) < 2:
            return "Gecersiz JWT formati"
        def pad(s):
            return s + "=" * (-len(s) % 4)
        header = base64.urlsafe_b64decode(pad(parts[0])).decode("utf-8", errors="replace")
        payload = base64.urlsafe_b64decode(pad(parts[1])).decode("utf-8", errors="replace")
        try:
            header = json.dumps(json.loads(header), indent=2, ensure_ascii=False)
        except Exception:
            pass
        try:
            payload = json.dumps(json.loads(payload), indent=2, ensure_ascii=False)
        except Exception:
            pass
        return "HEADER:\n{}\n\nPAYLOAD:\n{}".format(header, payload)
    except Exception as e:
        return "Hata: {}".format(e)
