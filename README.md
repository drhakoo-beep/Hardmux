# HARDMUX

A terminal-based (TUI) cybersecurity toolkit with arrow-key navigation, built for Termux, Kali Linux, and any Linux terminal.

## Features

- Full-screen terminal UI (`curses`) with a bold ASCII banner and boxed, arrow-key-driven menus
- Bilingual interface: English and Turkish
- Red color theme
- ~70 tools across 6 categories

## Tool Categories

| Category | Tools |
|---|---|
| OSINT | Username search (30+ platforms), social link generator, whois lookup, domain age, DNS lookup, IP info lookup, email format analysis, phone number analysis, Google dork generator |
| Network | Port scan (range), top-20 ports scan, single port TCP test, ping, ping sweep, host/reverse DNS info, traceroute, HTTP header analysis, SSL certificate info, banner grabber, subdomain enumeration, MAC vendor lookup, local network info |
| Hashing | MD5, SHA1, SHA224/256/384/512, SHA3-256/512, BLAKE2b/s, CRC32, Adler32, HMAC-SHA256, PBKDF2, salted SHA256, all-in-one hash generator |
| Encoding | Base64, Base32, Base85, Base58, Hex, Binary, URL, HTML entity, Unicode escape, Punycode, UUID generator, random token generator, JWT decoder |
| Ciphers | Caesar (+ bruteforce), Vigenere, Atbash, Rail Fence, XOR, ROT13, ROT47, Morse code, NATO phonetic, Leet speak, text reverse |
| Password Tools | Strength checker, common password check, entropy calculator, password generator, passphrase generator, PIN generator, wordlist generator |

## Requirements

- Python 3.8+
- A terminal that supports `curses` (default on Linux/Termux)

## Installation

### Termux (Android)

```bash
pkg update && pkg upgrade -y
pkg install python -y
pip install requests python-whois dnspython
git clone https://github.com/<your-username>/hardmux.git
cd hardmux
python main.py
```

### Kali Linux / Debian / Ubuntu

```bash
sudo apt update
sudo apt install python3 python3-pip traceroute -y
pip3 install requests python-whois dnspython
git clone https://github.com/<your-username>/hardmux.git
cd hardmux
python3 main.py
```

## Usage

- Use **Arrow Up / Arrow Down** (or `j` / `k`) to navigate menus
- Press **ENTER** to select
- Press **Q** or **ESC** to go back / exit
- When a tool needs input, type it and press **ENTER**

On first launch you will be asked to choose a language (Turkish or English).

## Project Structure

```
hardmux/
├── main.py
├── requirements.txt
├── core/
│   ├── ui.py            TUI engine: banner, boxed menus, prompts, result screen
│   └── lang.py           Turkish / English strings
└── modules/
    ├── osint.py           OSINT tools
    ├── network.py         Network / recon tools
    ├── hashing.py         Hash algorithms
    ├── encoding.py        Encoding / decoding tools
    ├── ciphers.py         Classical ciphers
    └── password_tools.py  Password utilities
```

## Notes

- All network and OSINT tools require an active internet connection where noted; some require the optional packages listed in `requirements.txt`.
- This tool is intended for use on systems and networks you own or have explicit authorization to test. You are responsible for complying with the laws that apply to you.

# Support

drhako42@gmail.com

## License

MIT License. Feel free to fork, modify, and open pull requests.
