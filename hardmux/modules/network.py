import socket
import subprocess
import platform
import ssl
import concurrent.futures

try:
    import requests
except ImportError:
    requests = None

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 6379: "Redis", 27017: "MongoDB",
}

TOP_20_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443,
                445, 993, 995, 1723, 3306, 3389, 5900, 8080]

SUBDOMAIN_WORDLIST = [
    "www", "mail", "ftp", "dev", "test", "staging", "api", "blog", "shop",
    "admin", "portal", "vpn", "ns1", "ns2", "m", "mobile", "webmail",
    "cpanel", "autodiscover", "cdn", "app", "beta", "docs", "status",
    "support", "secure", "static", "media", "images", "git",
]

OUI_TABLE = {
    "00:1A:2B": "Cisco Systems", "3C:5A:B4": "Apple", "F0:18:98": "Apple",
    "00:0C:29": "VMware", "08:00:27": "VirtualBox", "B8:27:EB": "Raspberry Pi",
    "DC:A6:32": "Raspberry Pi", "00:1B:63": "Apple", "A4:C3:F0": "Intel",
    "00:50:56": "VMware", "00:16:3E": "Xen",
}


def scan_port(target, port, timeout=1.0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            return port, result == 0
    except Exception:
        return port, False


def port_scan(target, port_range):
    try:
        start, end = port_range.split("-")
        start, end = int(start), int(end)
    except Exception:
        return "Gecersiz port araligi, orn: 1-1000"

    try:
        target_ip = socket.gethostbyname(target)
    except Exception as e:
        return "Cozumleme hatasi: {}".format(e)

    open_ports = []
    ports = range(start, end + 1)
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        futures = [executor.submit(scan_port, target_ip, p) for p in ports]
        for future in concurrent.futures.as_completed(futures):
            port, is_open = future.result()
            if is_open:
                service = COMMON_PORTS.get(port, "unknown")
                open_ports.append((port, service))

    open_ports.sort()
    if not open_ports:
        return "Hedef: {} ({})\nAcik port bulunamadi".format(target, target_ip)

    lines = ["Hedef: {} ({})".format(target, target_ip), "Acik Portlar:"]
    for port, service in open_ports:
        lines.append("  {}/tcp  {}".format(port, service))
    return "\n".join(lines)


def top_ports_scan(target):
    try:
        target_ip = socket.gethostbyname(target)
    except Exception as e:
        return "Cozumleme hatasi: {}".format(e)
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(scan_port, target_ip, p) for p in TOP_20_PORTS]
        for future in concurrent.futures.as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append((port, COMMON_PORTS.get(port, "unknown")))
    open_ports.sort()
    if not open_ports:
        return "Hedef: {} ({})\nYaygin portlarda acik port bulunamadi".format(target, target_ip)
    lines = ["Hedef: {} ({})".format(target, target_ip)]
    lines += ["  {}/tcp  {}".format(p, s) for p, s in open_ports]
    return "\n".join(lines)


def tcp_connect_test(target, port):
    try:
        port = int(port)
    except Exception:
        return "Gecersiz port"
    try:
        target_ip = socket.gethostbyname(target)
    except Exception as e:
        return "Cozumleme hatasi: {}".format(e)
    _, is_open = scan_port(target_ip, port, timeout=3.0)
    status = "ACIK / OPEN" if is_open else "KAPALI / CLOSED"
    return "Hedef: {} ({})\nPort {}: {}".format(target, target_ip, port, status)


def ping_host(host, count=3):
    system = platform.system().lower()
    if "windows" in system:
        cmd = ["ping", "-n", str(count), host]
    else:
        cmd = ["ping", "-c", str(count), host]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return "Ping hatasi: {}".format(e)


def ping_sweep(subnet_prefix):
    alive = []

    def check(ip):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                s.connect_ex((ip, 80))
            socket.gethostbyaddr(ip)
            return ip, True
        except socket.herror:
            return ip, True
        except Exception:
            return ip, False

    ips = ["{}.{}".format(subnet_prefix, i) for i in range(1, 255)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check, ip) for ip in ips]
        for future in concurrent.futures.as_completed(futures):
            ip, is_alive = future.result()
            if is_alive:
                alive.append(ip)
    alive.sort()
    if not alive:
        return "Aktif host bulunamadi"
    return "Aktif Hostlar:\n" + "\n".join(alive)


def host_info(target):
    lines = []
    try:
        ip = socket.gethostbyname(target)
        lines.append("IP: {}".format(ip))
    except Exception as e:
        return "Cozumleme hatasi: {}".format(e)
    try:
        hostname, aliases, addrs = socket.gethostbyaddr(ip)
        lines.append("Hostname: {}".format(hostname))
        if aliases:
            lines.append("Aliases: {}".format(", ".join(aliases)))
    except Exception:
        lines.append("Ters DNS bulunamadi")
    return "\n".join(lines)


def traceroute(target):
    system = platform.system().lower()
    cmd = ["tracert", target] if "windows" in system else ["traceroute", "-m", "20", target]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        out = result.stdout if result.stdout else result.stderr
        return out if out else "Cikti alinamadi"
    except FileNotFoundError:
        return "traceroute kurulu degil: pkg install traceroute"
    except Exception as e:
        return "Hata: {}".format(e)


def http_headers(url):
    if requests is None:
        return "requests modulu kurulu degil"
    if not url.startswith("http"):
        url = "https://" + url
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        lines = ["Status: {}".format(r.status_code)]
        lines += ["{}: {}".format(k, v) for k, v in r.headers.items()]
        return "\n".join(lines)
    except Exception as e:
        return "Hata: {}".format(e)


def ssl_cert_info(host, port=443):
    try:
        port = int(port)
    except Exception:
        port = 443
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=6) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
        lines = []
        for key, val in cert.items():
            lines.append("{}: {}".format(key, val))
        return "\n".join(lines) if lines else "Sertifika bilgisi alinamadi"
    except Exception as e:
        return "Hata: {}".format(e)


def banner_grab(host, port):
    try:
        port = int(port)
    except Exception:
        return "Gecersiz port"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(4)
            s.connect((host, port))
            try:
                s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            except Exception:
                pass
            data = s.recv(1024)
            return data.decode("utf-8", errors="replace") if data else "Banner alinamadi"
    except Exception as e:
        return "Hata: {}".format(e)


def subdomain_enum(domain):
    found = []

    def check(sub):
        fqdn = "{}.{}".format(sub, domain)
        try:
            ip = socket.gethostbyname(fqdn)
            return fqdn, ip
        except Exception:
            return None, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(check, sub) for sub in SUBDOMAIN_WORDLIST]
        for future in concurrent.futures.as_completed(futures):
            fqdn, ip = future.result()
            if fqdn:
                found.append("{} -> {}".format(fqdn, ip))
    found.sort()
    return "\n".join(found) if found else "Alt alan adi bulunamadi"


def mac_vendor_lookup(mac):
    mac = mac.strip().upper().replace("-", ":")
    prefix = ":".join(mac.split(":")[:3])
    vendor = OUI_TABLE.get(prefix, "Bilinmiyor / Unknown (yerel tablo sinirli)")
    return "MAC: {}\nOUI: {}\nVendor: {}".format(mac, prefix, vendor)


def local_network_info(_unused=None):
    lines = []
    hostname = socket.gethostname()
    lines.append("Hostname: {}".format(hostname))
    try:
        lines.append("Local IP: {}".format(socket.gethostbyname(hostname)))
    except Exception:
        lines.append("Local IP alinamadi")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        lines.append("Aktif Ag IP: {}".format(s.getsockname()[0]))
        s.close()
    except Exception:
        lines.append("Aktif ag IP alinamadi")
    return "\n".join(lines)
