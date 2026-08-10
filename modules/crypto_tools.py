import hashlib
import base64
import codecs
import urllib.parse


def hash_text(text):
    algos = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]
    lines = []
    data = text.encode("utf-8")
    for algo in algos:
        h = hashlib.new(algo)
        h.update(data)
        lines.append("{}: {}".format(algo.upper(), h.hexdigest()))
    return "\n".join(lines)


def b64_encode(text):
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def b64_decode(text):
    try:
        return base64.b64decode(text.encode("utf-8")).decode("utf-8", errors="replace")
    except Exception as e:
        return "Hata: {}".format(e)


def hex_encode(text):
    return text.encode("utf-8").hex()


def hex_decode(text):
    try:
        return bytes.fromhex(text.strip()).decode("utf-8", errors="replace")
    except Exception as e:
        return "Hata: {}".format(e)


def caesar_cipher(text, shift):
    try:
        shift = int(shift)
    except Exception:
        return "Gecersiz kaydirma degeri"
    result = []
    for ch in text:
        if ch.isupper():
            result.append(chr((ord(ch) - 65 + shift) % 26 + 65))
        elif ch.islower():
            result.append(chr((ord(ch) - 97 + shift) % 26 + 97))
        else:
            result.append(ch)
    return "".join(result)


def xor_cipher(text, key):
    if not key:
        return "Anahtar bos olamaz"
    data = text.encode("utf-8")
    key_bytes = key.encode("utf-8")
    result = bytes([data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data))])
    return result.hex()


def xor_decrypt_hex(hex_text, key):
    if not key:
        return "Anahtar bos olamaz"
    try:
        data = bytes.fromhex(hex_text.strip())
    except Exception as e:
        return "Hata: {}".format(e)
    key_bytes = key.encode("utf-8")
    result = bytes([data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data))])
    return result.decode("utf-8", errors="replace")


def rot13(text):
    return codecs.encode(text, "rot_13")


def url_encode(text):
    return urllib.parse.quote(text)


def url_decode(text):
    return urllib.parse.unquote(text)
