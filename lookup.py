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
    
    try:
        # Changed to a highly stable endpoint configuration
        response = requests.get(f"http://ip-api.com{ip}?fields=status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,proxy,hosting,query", timeout=8)
        data = response.json()
        
        if data.get("status") == "success":
            print(f"\n\033[38;5;201m[+] RESULTS FOR {data.get('query')}:\033[0m")
            print(f"  \033[38;5;93mCountry:\033[0m      {data.get('country')} ({data.get('countryCode')})")
            print(f"  \033[38;5;93mRegion/State:\033[0m {data.get('regionName')}")
            print(f"  \033[38;5;93mCity:\033[0m         {data.get('city')}")
            print(f"  \033[38;5;93mZip Code:\033[0m     {data.get('zip', 'N/A')}")
            print(f"  \033[38;5;93mLatitude:\033[0m     {data.get('lat')}")
            print(f"  \033[38;5;93mLongitude:\033[0m    {data.get('lon')}")
            print(f"  \033[38;5;93mTimezone:\033[0m     {data.get('timezone')}")
            print(f"  \033[38;5;93mISP:\033[0m          {data.get('isp')}")
            print(f"  \033[38;5;93mOrganization:\033[0m {data.get('org')}")
            print(f"  \033[38;5;93mASN:\033[0m          {data.get('as')}")
            
            # Checks if the target IP you searched is a VPN
            if data.get('proxy') or data.get('hosting') or "cloudflare" in str(data.get('isp')).lower():
                print(f"\n  \033[1;33m[!] Status: May be a vpn.\033[0m")
        else:
            print(f"\n\033[1;31m[-] IP Lookup Error: {data.get('message', 'Invalid entry')}\033[0m")
            
    except Exception:
        print("\n\033[1;31m[-] Network Error: The server blocked your machine's connection request.\033[0m")

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
