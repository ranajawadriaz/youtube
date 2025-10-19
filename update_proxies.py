#!/usr/bin/env python3
"""
Auto-update free proxies from public sources
Run this script periodically to keep proxies fresh
"""

import requests
import re
from typing import List

def fetch_free_proxies() -> List[str]:
    """Fetch working free proxies from multiple sources"""
    proxies = []
    
    print("Fetching free proxies...")
    
    # Source 1: proxy-list.download
    try:
        print("  - Checking proxy-list.download...")
        response = requests.get(
            "https://www.proxy-list.download/api/v1/get?type=http",
            timeout=10
        )
        if response.status_code == 200:
            proxy_ips = response.text.strip().split('\r\n')
            for ip in proxy_ips[:5]:  # Take first 5
                if ip and ':' in ip:
                    proxies.append(f"http://{ip}")
                    print(f"    ✓ Added: http://{ip}")
    except Exception as e:
        print(f"    ✗ Failed: {e}")
    
    # Source 2: free-proxy-list.net
    try:
        print("  - Checking free-proxy-list.net...")
        response = requests.get(
            "https://free-proxy-list.net/",
            timeout=10
        )
        if response.status_code == 200:
            # Parse HTML table
            matches = re.findall(r'<td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td>', response.text)
            for ip, port in matches[:5]:  # Take first 5
                proxies.append(f"http://{ip}:{port}")
                print(f"    ✓ Added: http://{ip}:{port}")
    except Exception as e:
        print(f"    ✗ Failed: {e}")
    
    # Source 3: geonode.com
    try:
        print("  - Checking geonode.com...")
        response = requests.get(
            "https://proxylist.geonode.com/api/proxy-list?limit=10&page=1&sort_by=lastChecked&sort_type=desc&protocols=http",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            for proxy in data.get('data', [])[:5]:
                ip = proxy.get('ip')
                port = proxy.get('port')
                if ip and port:
                    proxies.append(f"http://{ip}:{port}")
                    print(f"    ✓ Added: http://{ip}:{port}")
    except Exception as e:
        print(f"    ✗ Failed: {e}")
    
    return proxies

def test_proxy(proxy: str) -> bool:
    """Test if a proxy is working"""
    try:
        response = requests.get(
            "https://www.youtube.com",
            proxies={"http": proxy, "https": proxy},
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Free Proxy Updater for YouTube Transcript API")
    print("=" * 60)
    print()
    
    # Fetch proxies
    proxies = fetch_free_proxies()
    
    if not proxies:
        print("\n❌ No proxies found!")
        return
    
    print(f"\n✅ Found {len(proxies)} proxies")
    print("\nTesting proxies (this may take a minute)...")
    
    # Test proxies
    working_proxies = []
    for i, proxy in enumerate(proxies, 1):
        print(f"  [{i}/{len(proxies)}] Testing {proxy}...", end=" ")
        if test_proxy(proxy):
            print("✓ Working")
            working_proxies.append(proxy)
        else:
            print("✗ Failed")
    
    print(f"\n✅ {len(working_proxies)}/{len(proxies)} proxies are working")
    
    # Generate config
    if working_proxies:
        print("\n" + "=" * 60)
        print("Update enhanced_config.py with these proxies:")
        print("=" * 60)
        print("\nPROXY_LIST = [")
        for proxy in working_proxies:
            print(f'    "{proxy}",')
        print("]")
        print()
    else:
        print("\n⚠️  No working proxies found. Try running again later.")

if __name__ == "__main__":
    main()
