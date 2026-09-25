import os
import sys
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
    
    # Standard engineering format validation
    parts = ip.split('.')
    if len(parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
        print(f"\n\033[1;31m[-] Error: Invalid target IP address formatting profile.\033[0m")
        return
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }
    
    try:
        # Pull live operational coordinates 
        response = requests.get(f"https://ipapi.co{ip}/json/", headers=headers, timeout=8)
        
        if response.status_code == 429:
            print("\n\033[1;31m[-] Live Database Block: Your VPN provider has hit the lookup limit rate-ceiling. Try changing your VPN server node.\033[0m")
            return
        elif response.status_code != 200:
            print(f"\n\033[1;31m[-] Handshake Dropped: Server returned status code {response.status_code}.\033[0m")
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
            print(f"\n\033[1;31m[-] Database Error: {data.get('reason', 'Invalid execution parameters.')}\033[0m")
            
    except Exception as e:
        print("\n\033[1;31m[-] Connection Refused: Handshake timed out over the active tunnel routing system.\033[0m")

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
