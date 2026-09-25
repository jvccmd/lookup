import os
import sys
import time
import requests

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80

def print_banner():
    os.system('clear')
    width = get_terminal_width()
    
    m = "\033[38;5;201m" # Bright Magenta
    p = "\033[38;5;128m" # Purple
    i = "\033[38;5;93m"  # Indigo
    w = "\033[0m"         # Reset
    
    # Corrected ASCII block alignment for "INJURED LOOKUP"
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
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    try:
        # Request full dataset including hosting/proxy/security details
        response = requests.get(f"https://ipapi.co{ip}/json/", headers=headers, timeout=10)
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
            
            # Check if the IP network belongs to known datacenter ranges or cloud networks
            org_lower = str(data.get('org', '')).lower()
            known_vpns = ["cloudflare", "digitalocean", "amazon", "google", "linode", "ovh", "m247", "nordvpn", "expressvpn", "surfshark"]
            
            if any(vpn in org_lower for vpn in known_vpns):
                print(f"\n  \033[1;33m[!] Status: May be a vpn.\033[0m")
        else:
            print(f"\n\033[1;31m[-] Live Database Error: {data.get('reason', 'Invalid format execution.')}\033[0m")
            
    except Exception:
        print("\n\033[1;31m[-] Connection Refused: The live tracking server rejected the lookup.\033[0m")

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
