



root_url = 'https://www.whed.net/results_institutions.php'


payload = { 'Chp1': 'Afghanistan',
                'Chp0':'', 
                'Chp2':'',
                'Chp4': '',
                'nbr_ref_pge': '100',
                'debut' : '100'
                    }



cookies = {
        'PHPSESSID': '9195bbb4ni1td1v4t2ulodhmte',
    }

headers = {
        'authority': 'www.whed.net',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'PHPSESSID=9195bbb4ni1td1v4t2ulodhmte',
        'origin': 'https://www.whed.net',
        'referer': 'https://www.whed.net/results_institutions.php',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }
import requests
r = requests.get(root_url)
r = requests.get(root_url , params=payload)
print(r.url)