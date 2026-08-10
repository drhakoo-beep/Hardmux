import curses
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import ui
from core.lang import t
from modules import osint, network, hashing, encoding, ciphers, password_tools


def select_language(stdscr):
    ui.init_colors()
    options = ["Turkce", "English"]
    choice = ui.run_menu(stdscr, "SELECT LANGUAGE / DIL SECIN", options, "ARROWS + ENTER")
    return "tr" if choice == 0 else "en"


def run_action(stdscr, lang, title_key, prompt_keys, func, needs_labels=False, labels=None):
    args = []
    for pk in prompt_keys:
        val = ui.prompt_text(stdscr, t(lang, pk), t(lang, "type_hint"))
        args.append(val)
    if needs_labels:
        args.append(labels)
    try:
        result = func(*args)
    except Exception as e:
        result = "Hata / Error: {}".format(e)
    ui.show_result(stdscr, t(lang, title_key), str(result), t(lang, "press_enter"))


def generic_menu(stdscr, lang, menu_title_key, registry):
    while True:
        labels = [t(lang, key) for key, _, _, _ in registry] + [t(lang, "back")]
        choice = ui.run_menu(stdscr, t(lang, menu_title_key), labels, t(lang, "nav_hint"))
        if choice in (-1, len(registry)):
            return
        title_key, prompt_keys, func, needs_labels = registry[choice]
        run_action(stdscr, lang, title_key, prompt_keys, func, needs_labels)


def osint_menu(stdscr, lang):
    registry = [
        ("username_search", ["enter_username"], osint.username_search, False),
        ("social_link_gen", ["enter_username"], osint.social_link_generator, False),
        ("whois_lookup", ["enter_domain"], osint.whois_lookup, False),
        ("domain_age", ["enter_domain"], osint.domain_age, False),
        ("dns_lookup", ["enter_domain"], osint.dns_lookup, False),
        ("ip_lookup", ["enter_target"], osint.ip_lookup, False),
        ("email_lookup", ["enter_email"], osint.email_format_analysis, False),
        ("phone_analysis", ["enter_phone"], osint.phone_number_analysis, False),
        ("google_dork", ["enter_domain"], osint.google_dork_generator, False),
    ]
    generic_menu(stdscr, lang, "osint", registry)


def network_menu(stdscr, lang):
    registry = [
        ("port_scan", ["enter_target", "enter_port_range"], network.port_scan, False),
        ("top_ports", ["enter_target"], network.top_ports_scan, False),
        ("tcp_test", ["enter_target", "enter_port"], network.tcp_connect_test, False),
        ("ping_host", ["enter_target"], network.ping_host, False),
        ("ping_sweep", ["enter_subnet"], network.ping_sweep, False),
        ("host_info", ["enter_target"], network.host_info, False),
        ("traceroute", ["enter_target"], network.traceroute, False),
        ("http_headers", ["enter_url"], network.http_headers, False),
        ("ssl_info", ["enter_target"], network.ssl_cert_info, False),
        ("banner_grab", ["enter_target", "enter_port"], network.banner_grab, False),
        ("subdomain_enum", ["enter_domain"], network.subdomain_enum, False),
        ("mac_vendor", ["enter_mac"], network.mac_vendor_lookup, False),
        ("local_net", [], network.local_network_info, False),
    ]
    generic_menu(stdscr, lang, "network", registry)


def hashing_menu(stdscr, lang):
    registry = [
        ("hash_all", ["enter_text"], hashing.hash_all, False),
        ("md5", ["enter_text"], hashing.md5_hash, False),
        ("sha1", ["enter_text"], hashing.sha1_hash, False),
        ("sha224", ["enter_text"], hashing.sha224_hash, False),
        ("sha256", ["enter_text"], hashing.sha256_hash, False),
        ("sha384", ["enter_text"], hashing.sha384_hash, False),
        ("sha512", ["enter_text"], hashing.sha512_hash, False),
        ("sha3_256", ["enter_text"], hashing.sha3_256_hash, False),
        ("sha3_512", ["enter_text"], hashing.sha3_512_hash, False),
        ("blake2b", ["enter_text"], hashing.blake2b_hash, False),
        ("blake2s", ["enter_text"], hashing.blake2s_hash, False),
        ("crc32", ["enter_text"], hashing.crc32_checksum, False),
        ("adler32", ["enter_text"], hashing.adler32_checksum, False),
        ("hmac256", ["enter_text", "enter_key"], hashing.hmac_sha256, False),
        ("pbkdf2", ["enter_text", "enter_salt"], hashing.pbkdf2_demo, False),
        ("salted", ["enter_text", "enter_salt"], hashing.salted_sha256, False),
    ]
    generic_menu(stdscr, lang, "hashing", registry)


def encoding_menu(stdscr, lang):
    registry = [
        ("b64_encode", ["enter_text"], encoding.b64_encode, False),
        ("b64_decode", ["enter_text"], encoding.b64_decode, False),
        ("b32_encode", ["enter_text"], encoding.b32_encode, False),
        ("b32_decode", ["enter_text"], encoding.b32_decode, False),
        ("b85_encode", ["enter_text"], encoding.b85_encode, False),
        ("b85_decode", ["enter_text"], encoding.b85_decode, False),
        ("b58_encode", ["enter_text"], encoding.base58_encode, False),
        ("b58_decode", ["enter_text"], encoding.base58_decode, False),
        ("hex_encode", ["enter_text"], encoding.hex_encode, False),
        ("hex_decode", ["enter_text"], encoding.hex_decode, False),
        ("bin_encode", ["enter_text"], encoding.binary_encode, False),
        ("bin_decode", ["enter_text"], encoding.binary_decode, False),
        ("url_encode", ["enter_text"], encoding.url_encode, False),
        ("url_decode", ["enter_text"], encoding.url_decode, False),
        ("html_encode", ["enter_text"], encoding.html_encode, False),
        ("html_decode", ["enter_text"], encoding.html_decode, False),
        ("uni_encode", ["enter_text"], encoding.unicode_escape_encode, False),
        ("uni_decode", ["enter_text"], encoding.unicode_escape_decode, False),
        ("puny_encode", ["enter_text"], encoding.punycode_encode, False),
        ("puny_decode", ["enter_text"], encoding.punycode_decode, False),
        ("uuid_gen", [], encoding.uuid_generate, False),
        ("token_gen", ["enter_length"], encoding.random_token, False),
        ("token_urlsafe", ["enter_length"], encoding.random_urlsafe_token, False),
        ("jwt_decode", ["enter_jwt"], encoding.jwt_decode, False),
    ]
    generic_menu(stdscr, lang, "encoding", registry)


def ciphers_menu(stdscr, lang):
    registry = [
        ("caesar", ["enter_text", "enter_shift"], ciphers.caesar_cipher, False),
        ("caesar_brute", ["enter_text"], ciphers.caesar_bruteforce, False),
        ("vigenere_enc", ["enter_text", "enter_key"], ciphers.vigenere_encode, False),
        ("vigenere_dec", ["enter_text", "enter_key"], ciphers.vigenere_decode, False),
        ("atbash", ["enter_text"], ciphers.atbash_cipher, False),
        ("railfence_enc", ["enter_text", "enter_rails"], ciphers.rail_fence_encode, False),
        ("railfence_dec", ["enter_text", "enter_rails"], ciphers.rail_fence_decode, False),
        ("xor_enc", ["enter_text", "enter_key"], ciphers.xor_cipher, False),
        ("xor_dec", ["enter_text", "enter_key"], ciphers.xor_decrypt_hex, False),
        ("rot13", ["enter_text"], ciphers.rot13, False),
        ("rot47", ["enter_text"], ciphers.rot47, False),
        ("morse_enc", ["enter_text"], ciphers.morse_encode, False),
        ("morse_dec", ["enter_text"], ciphers.morse_decode, False),
        ("nato", ["enter_text"], ciphers.nato_encode, False),
        ("leet", ["enter_text"], ciphers.leet_encode, False),
        ("reverse", ["enter_text"], ciphers.reverse_text, False),
    ]
    generic_menu(stdscr, lang, "ciphers", registry)


def password_menu(stdscr, lang):
    labels = {
        "weak": t(lang, "weak"), "medium": t(lang, "medium"),
        "strong": t(lang, "strong"), "very_strong": t(lang, "very_strong"),
    }
    registry = [
        ("pass_check", ["enter_password"], password_tools.check_strength, True),
        ("pass_common", ["enter_password"], password_tools.common_password_check, False),
        ("pass_entropy", ["enter_password"], password_tools.password_entropy, False),
        ("pass_gen", ["enter_length"], password_tools.generate_password, False),
        ("pass_phrase", ["enter_word_count"], password_tools.generate_passphrase, False),
        ("pass_pin", ["enter_length"], password_tools.generate_pin, False),
        ("pass_wordlist", ["enter_words"], password_tools.generate_wordlist, False),
    ]
    while True:
        opts = [t(lang, key) for key, _, _, _ in registry] + [t(lang, "back")]
        choice = ui.run_menu(stdscr, t(lang, "password"), opts, t(lang, "nav_hint"))
        if choice in (-1, len(registry)):
            return
        title_key, prompt_keys, func, needs_labels = registry[choice]
        run_action(stdscr, lang, title_key, prompt_keys, func, needs_labels, labels)


def main_menu(stdscr, lang):
    while True:
        options = [
            t(lang, "osint"), t(lang, "network"), t(lang, "hashing"),
            t(lang, "encoding"), t(lang, "ciphers"), t(lang, "password"),
            t(lang, "exit"),
        ]
        choice = ui.run_menu(stdscr, t(lang, "main_menu"), options, t(lang, "nav_hint"))
        if choice in (-1, 6):
            return
        if choice == 0:
            osint_menu(stdscr, lang)
        elif choice == 1:
            network_menu(stdscr, lang)
        elif choice == 2:
            hashing_menu(stdscr, lang)
        elif choice == 3:
            encoding_menu(stdscr, lang)
        elif choice == 4:
            ciphers_menu(stdscr, lang)
        elif choice == 5:
            password_menu(stdscr, lang)


def run(stdscr):
    lang = select_language(stdscr)
    main_menu(stdscr, lang)


if __name__ == "__main__":
    curses.wrapper(run)
