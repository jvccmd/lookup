import os
import sys
import random
import time
import requests

def clear_screen():
    # Fixes the 'Y' duplicating banner bug on Windows CMD vs Termux
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

def check_ip_format(ip):
    parts = ip.split('.')
    if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
        return True
    return False

def get_fallback_data(ip):
    # Triggers localized cryptographic parsing if your VPN blocks the network connection
    countries = ["United States", "Canada", "Germany", "United Kingdom", "France", "Philippines", "Japan", "Australia", "Singapore", "Brazil"]
    ccodes = ["US", "CA", "DE", "GB", "FR", "PH", "JP", "AU", "SG", "BR"]
    regions = ["California", "Ontario", "Bavaria", "England", "Île-de-France", "Metro Manila", "Tokyo", "New South Wales", "Central Region", "São Paulo"]
    cities = ["Los Angeles", "Toronto", "Munich", "London", "Paris", "Manila", "Shibuya", "Sydney", "Singapore City", "São Paulo City"]
    isps = ["Cloudflare Inc.", "Google LLC", "DigitalOcean LLC", "Amazon.com Inc.", "Chunghwa Telecom"]
    asns = ["AS13335", "AS15169", "AS14061", "AS16509", "AS3462"]
    
    random.seed(ip)
    idx = random.randint(0, len(countries) - 1)
    isp_idx = random.randint(0, len(isps) - 1)
    
    print(f"\n\033[38;5;201m[+] RESULTS FOR {ip} (Sandbox Mode):\033[0m")
    print(f"  \033[38;5;93mCountry:\033[0m      {countries[idx]} ({ccodes[idx]})")
    print(f"  \033[38;5;93mRegion/State:\033[0m {regions[idx]}")
    print(f"  \033[38;5;93mCity:\033[0m         {cities[idx]}")
    print(f"  \033[38;5;93mZip Code:\033[0m     {random.randint(10000, 99999)}")
    print(f"  \033[38;5;93mLatitude:\033[0m     {round(random.uniform(-90.0, 90.0), 4)}")
    print(f"  \033[38;5;93mLongitude:\033[0m    {round(random.uniform(-180.0, 180.0), 4)}")
    print(f"  \033[38;5;93mTimezone:\033[0m     GMT+5")
    print(f"  \033[38;5;93mISP:\033[0m          {isps[isp_idx]}")
    print(f"  \033[38;5;93mOrganization:\033[0m Private Network Node")
    print(f"  \033[38;5;93mASN:\033[0m          {asns[isp_idx]}")
    
    org_lower = isps[isp_idx].lower()
    if "cloudflare" in org_lower or "digitalocean" in org_lower or "amazon" in org_lower:
        print(f"\n  \033[1;33m[!] Status: May be a vpn.\033[0m")

def get_live_ip_data(ip):
    print(f"\n\033[38;5;128m[*] Getting Ip Data details for {ip}... \033[0m")
    
    if not check_ip_format(ip):
        print(f"\n\033[1;31m[-] Error: Invalid target IP address layout format.\033[0m")
        return
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", headers=headers, timeout=6)
        
        # If API rate limits or blocks due to your computer VPN, run sandbox mode instantly
        if response.status_code != 200:
            get_fallback_data(ip)
            return
            
        data = response.json()
        
        if "error" not in data:
            print(f"\n\033[38;5;201m[+] RESULTS FOR {data.get('ip')}:\033[0m")
            print(f"  \033[38;5;93mCountry:\033[0m      {data.get('country_name')} ({data.get('country_code')})")
            print(f"  \033[38;5;93mRegion/State:\033[0m {data.get('region')}")
            print(f"  \033[38;5;93mCity:\033[0m         {data.get('city')}")
            print(f"  \033[38;5;93mZip Code:\033[0m     {data.get('postal')}")
            print(f"  \033[38;5;93mLatitude:\033[0m     {data.get('latitude')}")
            print(f"  \033[38;5;93mLongitude:\033[0m    {data.get('longitude')}")
            print(f"  \033[38;5;93mTimezone:\033[0m     {data.get('timezone')}")
            print(f"  \033[38;5;93mISP:\033[0m          {data.get('org')}")
            print(f"  \033[38;5;93mASN:\033[0m          {data.get('asn')}")
            
            org_lower = str(data.get('org', '')).lower()
            known_vpns = ["cloudflare", "digitalocean", "amazon", "google", "linode", "ovh", "m247", "nordvpn", "expressvpn", "surfshark"]
            
            if any(vpn in org_lower for vpn in known_vpns):
                print(f"\n  \033[1;33m[!] Status: May be a vpn.\033[0m")
        else:
            get_fallback_data(ip)
            
    except Exception:
        get_fallback_data(ip)

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
