import requests
import sys
import json
import yaml
from urllib.parse import urlparse, parse_qs

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


def breach_collection(host, api_key):
#email domain query
    send = {"type": 2,
            "query": host
            }
    headers = {'Authorization': f'Bearer {api_key}'}

    r = requests.post("https://breachcollection.com/api/get-credentials", data=send, headers=headers)
    
    r.raise_for_status()

    result_temp = r.json()
    result_email_domain = []

    for row in result_temp:
        sublist = []
        for element in row:
            sublist.append(element)
        result_email_domain.append(sublist)


#domain query
    send = {"type": 0,
            "query": host
            }
    headers = {'Authorization': f'Bearer {api_key}'}

    r = requests.post("https://breachcollection.com/api/get-credentials", data=send, headers=headers)
    r.raise_for_status()

    result_temp = r.json()
    result_domain = []
    for row in result_temp:
        sublist = []
        for element in row:
            sublist.append(element)
        result_domain.append(sublist)



    
    return [result_email_domain, result_domain]
    

def param_finder(urls):
    unique_params = set()
    
    for url in urls:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        for param in query_params.keys():
            unique_params.add(param)
    
    return unique_params





if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 2 or argc > 3:
        print('Usage:\n\tpython3 nextrecon.py <domain> [include_subdomains:true/false]')
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


    print("")
    print("")
    print(r"""888b    888                   888    8888888b.                                    
8888b   888                   888    888   Y88b                                   
88888b  888                   888    888    888                                   
888Y88b 888  .d88b.  888  888 888888 888   d88P .d88b.   .d8888b .d88b.  88888b.  
888 Y88b888 d8P  Y8b `Y8bd8P' 888    8888888P" d8P  Y8b d88P"   d88""88b 888 "88b 
888  Y88888 88888888   X88K   888    888 T88b  88888888 888     888  888 888  888 
888   Y8888 Y8b.     .d8""8b. Y88b.  888  T88b Y8b.     Y88b.   Y88..88P 888  888 
888    Y888  "Y8888  888  888  "Y888 888   T88b "Y8888   "Y8888P "Y88P"  888  888 
                                                                                  
                                                                                  
                                                                                  """)


    print("")
    print("")

        #open config file and get all the api keys
    key_bc = None

    try:
        with open("config.yaml", 'r') as config_file:
            confs = yaml.safe_load(config_file)
        key_bc = None
        key_bc = confs.get('breachcollection_api_key')
        if (key_bc == "" or key_bc==None):
            print("No BreachCollection API Key found! Add it in the config.yaml file.")

    except FileNotFoundError:
        print("No config.yaml file found!")

    except yaml.YAMLError as e:
        print("API key(s) missing!")

    if (key_bc):
        leaks = breach_collection(host, key_bc)
        filename = f"{host}-leaks.txt"

        with open(filename, 'w') as file:
            if len(leaks[0]) > 0 or len(leaks[1]) > 0:
                print("[*]======CREDENTIALS FOUND======", file=file)

            if len(leaks[0]) > 0:
                print("[*]===EMAIL DOMAIN RESULTS===", file=file)

                for leak in leaks[0]:
                    if len(leak) >= 3:
                        print(f"URL: {leak[0]}", file=file)
                        print(f"Username: {leak[1]}", file=file)
                        print(f"Password: {leak[2]}", file=file)
                        print("", file=file)


            if len(leaks[1]) > 3:
                print("[*]===DOMAIN RESULTS===", file=file)

                for leak in leaks[1]:
                    if len(leak) >= 3:

                        print(f"URL: {leak[0]}", file=file)
                    
                        print(f"Username: {leak[1]}", file=file)
                    
                        print(f"Password: {leak[2]}", file=file)
                    
                        print("", file=file)

        print(f"[*]Leaks found written to {host}-leaks.txt")


    urls = waybackurls(host, with_subs)
    
    if urls:
        filename = f'{host.replace("://", "_").replace("/", "_")}-all_urls.txt'
        with open(filename, 'w') as f:
            for url in urls:
                f.write(url + '\n')
        print(f'[*] Saved {len(urls)} URLs to {filename}')

        params = param_finder(urls)
        filename = f'{host.replace("://", "_").replace("/", "_")}-params.txt'
        with open(filename, 'w') as f:
            for param in params:
                f.write(param + '\n')
        print(f'[*] Saved {len(params)} Parameters to {filename}')


    else:
        print('[-] Found no URLs')

    


    






