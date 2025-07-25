import requests
import sys
import json

def waybackurls(host, with_subs):
    if with_subs:
        url = f'http://web.archive.org/cdx/search/cdx?url=*.{host}/*&output=csv&fl=original&collapse=urlkey'
    else:
        url = f'http://web.archive.org/cdx/search/cdx?url={host}/*&output=csv&fl=original&collapse=urlkey'
    
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        lines = r.text.strip().split('\n')
        if not lines or (len(lines) == 1 and not lines[0]):
            return []


        urls = []
        for line in lines:
            if line:
                urls.append(line.split(',')[0])

        return urls

    except requests.exceptions.Timeout:
        print(f"Error fetching data: Request timed out for {host}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {host}: {e}")
        return []

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 2 or argc > 3:
        print('Usage:\n\tpython3 waybackurls.py <url> [include_subdomains:true/false]')
        sys.exit()

    host = sys.argv[1]
    with_subs = False
    if argc == 3:
        if sys.argv[2].lower() == 'true':
            with_subs = True
        elif sys.argv[2].lower() == 'false':
            with_subs = False
        else:
            print('Invalid value for include_subdomains. Use "true" or "false".')
            sys.exit()

    urls = waybackurls(host, with_subs)
    
    if urls:
        filename = f'{host.replace("://", "_").replace("/", "_")}-all_urls.txt'
        with open(filename, 'w') as f:
            for url in urls:
                f.write(url + '\n')
        print(f'[*] Saved {len(urls)} results to {filename}')
    else:
        print('[-] Found nothing')

    