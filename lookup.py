import os
import sys
import json
import requests

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80

def print_banner():
    clear_screen()
    width = get_terminal_width()
    
    m = "\033[38;5;201m" # Bright Magenta
    p = "\033[38;5;128m" # Purple
    i = "\033[38;5;93m"  # Indigo
    w = "\033[0m"         # Reset
    
    raw_lines = [
        "██ ███    ██      ██ ██    ██ ██████  ███████ ██████  ",
        "██ ████   ██      ██ ██    ██ ██   ██ ██      ██   ██ ",
        "██ ██ ██  ██      ██ ██    ██ ██████  █████   ██   ██ ",
        "██ ██  ██ ██ ██   ██ ██    ██ ██   ██ ██      ██   ██ ",
        "██ ██   ████  █████   ██████  ██   ██ ███████ ██████  ",
        "",
        "██      ██████   ██████  ██   ██ ██    ██ ██████  ",
        "██     ██    ██ ██    ██ ██  ██  ██    ██ ██   ██ ",
        "██     ██    ██ ██    ██ █████   ██    ██ ██████  ",
        "██     ██    ██ ██    ██ ██  ██  ██    ██ ██      ",
        "███████ ██████   ██████  ██   ██  ██████  ██      "
    ]
    
    colored_lines = [
        f"{m}██ ███    ██{p}      ██ ██{i}    ██ ██████  ███████ ██████  {w}",
        f"{m}██ ████   ██{p}      ██ ██{i}    ██ ██   ██ ██      ██   ██ {w}",
        f"{m}██ ██ ██  ██{p}      ██ ██{i}    ██ ██████  █████   ██   ██ {w}",
        f"{m}██ ██  ██ ██{p} ██   ██ ██{i}    ██ ██   ██ ██      ██   ██ {w}",
        f"{m}██ ██   ████{p}  █████   {i}██████  ██   ██ ███████ ██████  {w}",
        "",
        f"{m}██      ██████  {p} ██████  ██   ██{i} ██    ██ ██████  {w}",
        f"{m}██     ██    ██ {p}██    ██ ██  ██ {i}██    ██ ██   ██ {w}",
        f"{m}██     ██    ██ {p}██    ██ █████  {i}██    ██ ██████  {w}",
        f"{m}██     ██    ██ {p}██    ██ ██  ██ {i}██    ██ ██      {w}",
        f"{m}███████ ██████  {p} ██████{i}  ██   ██  ██████  ██      {w}"
    ]
    
    for raw, colored in zip(raw_lines, colored_lines):
        if raw == "":
            print("")
        else:
            padding = max(0, (width - len(raw)) // 2)
            print(" " * padding + colored)
    print("\n")

def get_live_ip_data(ip):
    print(f"\n\033[38;5;128m[*] Getting Ip Data details for {ip}... \033[0m")
    
    parts = ip.split('.')
    if len(parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
        print(f"\n\033[1;31m[-] Error: Invalid target IP address layout format.\033[0m")
        return
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/dns-json"
    }
    
    try:
        # Reversing IP for DNS pointer lookup over Cloudflare's secure DNS network
        rev_ip = ".".join(reversed(parts))
        url = f"https://1.1.1{rev_ip}.in-addr.arpa&type=PTR"
        
        response = requests.get(url, headers=headers, timeout=10)
        dns_data = response.json()
        
        hostname = "N/A"
        if "Answer" in dns_data:
            hostname = dns_data["Answer"][0]["data"].rstrip('.')

        # Getting the live location info over a high-capacity secure CDN bridge
        geo_url = f"https://ripe.net{ip}"
        geo_response = requests.get(geo_url, timeout=10)
        
        country = "N/A"
        org = "N/A"
        
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            country = geo_data.get("country", "N/A")
            org = geo_data.get("name", "N/A")

        # Running backup live query pool if primary CDN bridge leaves fields blank
        if country == "N/A" or country == "":
            fallback = requests.get(f"https://ipapi.co{ip}/json/", headers={"User-Agent": "Mozilla"}, timeout=5).json()
            country = fallback.get("country_name", "N/A")
            org = fallback.get("org", "N/A")

        print(f"\n\033[38;5;201m[+] RESULTS FOR {ip}:\033[0m")
        print(f"  \033[38;5;93mCountry:\033[0m      {country}")
        print(f"  \033[38;5;93mISP/Host:\033[0m    {org}")
        print(f"  \033[38;5;93mHostname:\033[0m    {hostname}")
        
        if "cloudflare" in org.lower() or "vpn" in org.lower() or "hosting" in hostname.lower():
            print(f"\n  \033[1;33m[!] Status: May be a vpn.\033[0m")
            
    except Exception:
        print("\n\033[1;31m[-] Error: The server dropped the request. Secure handshake failed.\033[0m")

def main():
    while True:
        print_banner()
        
        ip_input = input("\033[38;5;128mEnter ip to search > \033[0m").strip()
        
        if ip_input:
            get_live_ip_data(ip_input)
        else:
            print("\n\033[1;31m[-] No IP provided.\033[0m")
        
        print("\n" + "\033[38;5;93m-\033[0m"*50)
        choice = input("\033[38;5;128m[+] Completed, Press Y/N to go back to home or not > \033[0m").strip().lower()
        
        if choice == 'y':
            continue
        elif choice == 'n':
            print("\033[1;31mExiting...\033[0m")
            break
        else:
            continue

if __name__ == "__main__":
    main()
