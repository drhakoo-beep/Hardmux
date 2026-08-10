MORSE_TABLE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': '/',
}
MORSE_REVERSE = {v: k for k, v in MORSE_TABLE.items()}

NATO_TABLE = {
    'A': 'Alfa', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo',
    'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliett',
    'K': 'Kilo', 'L': 'Lima', 'M': 'Mike', 'N': 'November', 'O': 'Oscar',
    'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
    'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'Xray', 'Y': 'Yankee',
    'Z': 'Zulu', '0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three',
    '4': 'Four', '5': 'Five', '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine',
}

LEET_TABLE = str.maketrans("aeostAEOST", "4307584307")


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


def caesar_bruteforce(text):
    lines = []
    for shift in range(1, 26):
        lines.append("Shift {}: {}".format(shift, caesar_cipher(text, shift)))
    return "\n".join(lines)


def vigenere_encode(text, key):
    if not key or not key.isalpha():
        return "Anahtar sadece harflerden olusmali"
    key = key.upper()
    result = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[ki % len(key)]) - 65
            base = 65 if ch.isupper() else 97
            result.append(chr((ord(ch) - base + shift) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return "".join(result)


def vigenere_decode(text, key):
    if not key or not key.isalpha():
        return "Anahtar sadece harflerden olusmali"
    key = key.upper()
    result = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[ki % len(key)]) - 65
            base = 65 if ch.isupper() else 97
            result.append(chr((ord(ch) - base - shift) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return "".join(result)


def atbash_cipher(text):
    result = []
    for ch in text:
        if ch.isupper():
            result.append(chr(90 - (ord(ch) - 65)))
        elif ch.islower():
            result.append(chr(122 - (ord(ch) - 97)))
        else:
            result.append(ch)
    return "".join(result)


def rail_fence_encode(text, rails):
    try:
        rails = int(rails)
    except Exception:
        return "Gecersiz ray sayisi"
    if rails < 2:
        return "Ray sayisi en az 2 olmali"
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    for ch in text:
        fence[rail].append(ch)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    return "".join("".join(row) for row in fence)


def rail_fence_decode(text, rails):
    try:
        rails = int(rails)
    except Exception:
        return "Gecersiz ray sayisi"
    if rails < 2:
        return "Ray sayisi en az 2 olmali"
    pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
    if not pattern:
        pattern = [0]
    indices = [pattern[i % len(pattern)] for i in range(len(text))]
    order = sorted(range(len(text)), key=lambda i: indices[i])
    result = [""] * len(text)
    for pos, idx in zip(order, range(len(text))):
        result[pos] = text[idx]
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
    import codecs
    return codecs.encode(text, "rot_13")


def rot47(text):
    result = []
    for ch in text:
        code = ord(ch)
        if 33 <= code <= 126:
            result.append(chr(33 + ((code + 14) % 94)))
        else:
            result.append(ch)
    return "".join(result)


def morse_encode(text):
    return " ".join(MORSE_TABLE.get(ch.upper(), "") for ch in text if ch.upper() in MORSE_TABLE or ch == " ")


def morse_decode(text):
    words = text.strip().split(" / ")
    result = []
    for word in words:
        letters = word.strip().split()
        result.append("".join(MORSE_REVERSE.get(l, "") for l in letters))
    return " ".join(result)


def nato_encode(text):
    return " ".join(NATO_TABLE.get(ch.upper(), ch) for ch in text)


def leet_encode(text):
    return text.translate(LEET_TABLE)


def reverse_text(text):
    return text[::-1]
