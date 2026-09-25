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
    
    parts = ip.split('.')
    if len(parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
        print(f"\n\033[1;31m[-] Error: Invalid target IP address layout format.\033[0m")
        return
        
    try:
        # Targeting ipinfo's public unthrottled line (matches premium geo registries closely)
        url = f"https://ipinfo.io{ip}/json"
        response = requests.get(url, timeout=6)
        data = response.json()
        
        if response.status_code == 200 and "banned" not in str(data).lower():
            # Translate raw country codes to clean names
            ccode = data.get('country', 'N/A')
            country = "Philippines" if ccode == "PH" else ccode
            
            loc = data.get('loc', '').split(',')
            lat = loc[0] if len(loc) > 0 else 'N/A'
            lon = loc[1] if len(loc) > 1 else 'N/A'
            isp = data.get('org', 'N/A')
            
            print(f"\n\033[38;5;201m[+] RESULTS FOR {data.get('ip')}:\033[0m")
            print(f"  \033[38;5;93mCountry:\033[0m      {country} ({ccode})")
            print(f"  \033[38;5;93mRegion/State:\033[0m {data.get('region', 'N/A')}")
            print(f"  \033[38;5;93mCity:\033[0m         {data.get('city', 'N/A')}")
            print(f"  \033[38;5;93mZip Code:\033[0m     {data.get('postal', 'N/A')}")
            print(f"  \033[38;5;93mLatitude:\033[0m     {lat}")
            print(f"  \033[38;5;93mLongitude:\033[0m    {lon}")
            print(f"  \033[38;5;93mTimezone:\033[0m     {data.get('timezone', 'N/A')}")
            print(f"  \033[38;5;93mISP:\033[0m          {isp}")
            print(f"  \033[38;5;93mOrganization:\033[0m {isp}")
            
            if any(x in isp.lower() for x in ["cloudflare", "vpn", "hosting", "server"]):
                print(f"\n  \033[1;33m[!] Status: May be a vpn.\033[0m")
        else:
            print("\n\033[1;31m[-] Lookup Error: The server rejected the query parameters.\033[0m")
            
    except Exception:
        print("\n\033[1;31m[-] Network Error: Connection blocked. Handshake failed.\033[0m")

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
