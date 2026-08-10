import hashlib
import zlib
import hmac as hmac_lib


def _hash(text, algo):
    h = hashlib.new(algo)
    h.update(text.encode("utf-8"))
    return h.hexdigest()


def md5_hash(text):
    return _hash(text, "md5")


def sha1_hash(text):
    return _hash(text, "sha1")


def sha224_hash(text):
    return _hash(text, "sha224")


def sha256_hash(text):
    return _hash(text, "sha256")


def sha384_hash(text):
    return _hash(text, "sha384")


def sha512_hash(text):
    return _hash(text, "sha512")


def sha3_256_hash(text):
    return _hash(text, "sha3_256")


def sha3_512_hash(text):
    return _hash(text, "sha3_512")


def blake2b_hash(text):
    return hashlib.blake2b(text.encode("utf-8")).hexdigest()


def blake2s_hash(text):
    return hashlib.blake2s(text.encode("utf-8")).hexdigest()


def crc32_checksum(text):
    return format(zlib.crc32(text.encode("utf-8")) & 0xFFFFFFFF, "08x")


def adler32_checksum(text):
    return format(zlib.adler32(text.encode("utf-8")) & 0xFFFFFFFF, "08x")


def hmac_sha256(text, key):
    if not key:
        return "Anahtar bos olamaz"
    return hmac_lib.new(key.encode("utf-8"), text.encode("utf-8"), hashlib.sha256).hexdigest()


def pbkdf2_demo(text, salt):
    if not salt:
        salt = "hardmux"
    derived = hashlib.pbkdf2_hmac("sha256", text.encode("utf-8"), salt.encode("utf-8"), 100000)
    return "Salt: {}\nIterasyon: 100000\nSonuc: {}".format(salt, derived.hex())


def salted_sha256(text, salt):
    if not salt:
        salt = "hardmux"
    combined = (salt + text).encode("utf-8")
    return "Salt: {}\nHash: {}".format(salt, hashlib.sha256(combined).hexdigest())


def hash_all(text):
    algos = [
        ("MD5", md5_hash), ("SHA1", sha1_hash), ("SHA224", sha224_hash),
        ("SHA256", sha256_hash), ("SHA384", sha384_hash), ("SHA512", sha512_hash),
        ("SHA3-256", sha3_256_hash), ("SHA3-512", sha3_512_hash),
        ("BLAKE2b", blake2b_hash), ("BLAKE2s", blake2s_hash),
    ]
    lines = ["{}: {}".format(name, fn(text)) for name, fn in algos]
    lines.append("CRC32: {}".format(crc32_checksum(text)))
    lines.append("Adler32: {}".format(adler32_checksum(text)))
    return "\n".join(lines)
