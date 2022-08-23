from cmath import log
from curses import meta
from distutils.log import debug
from email import header
from wsgiref import headers

import cupshelpers
import debian
from pkg_resources import yield_lines
from pytz import country_names
import scrapy
import requests
import logging
from scrapy import FormRequest
logging.basicConfig(filename="log.txt", level=logging.DEBUG)

class WHEDSPIDER(scrapy.Spider):
    name = "World_higher_education_database"
    root_url = 'https://www.whed.net/results_institutions.php'
    payload = { 'Chp1': '',
                'Chp0':'', 
                'Chp2':'',
                'Chp4': '',
                'nbr_ref_pge': '100',
                'debut' : ''
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


    def start_requests(self):
            yield scrapy.Request(url=self.root_url, callback=self.parse_counteries_names)


    def parse_counteries_names(self,response):
        logging.debug('####################### in parse_counteries_names function#####################################')
        Country_names = response.xpath('//select[@id="Chp1"]/option/text()').getall()

        for index in range(1 , len(Country_names)):
            
            self.payload['Chp1'] = Country_names[index]
            print(self.payload)
            
            yield FormRequest(
                    url=self.root_url,
                    method="POST",
                    formdata=self.payload,
                    callback=self.parse_universites_name,
                    cookies=self.cookies,
                    headers=self.headers
                )
            break
    def parse_page_handler(self,response):
        
        print(f'parse_page_handler has been called')
        self.payload['debut'] = '100'
        # print(self.payload)

        yield FormRequest(
                    url=self.root_url,
                    method="POST",
                    formdata=self.payload,
                    callback=self.parse_universites_name,
                    cookies=self.cookies,
                    headers=self.headers
                )




    def parse_universites_name(self,response ):
        print(f'universities link of country : {response.url}')
        # logging.debug('this is response : ',response)
        Total_Universites = int(response.xpath('//*[@id="contenu"]/form[2]/div/p/text()').get().split(' ')[-1])
        
        print(f' Universites lenght {Total_Universites}')
  

        for index in range(1, Total_Universites):
            X_Path_Universites_Name = f'//*[@id="results"]/li[{index}]/div[2]/h3/a/text()'
            University_Name = response.xpath(X_Path_Universites_Name).get()
            
            print(f'University Name : {University_Name}')
            if University_Name is None:
                response.meta['count'] = index

                yield scrapy.Request(url = self.root_url , callback=self.parse_page_handler,dont_filter=True )

        # universities = response.xpath('//*[@title="More details"]/text()').getall()
        # universities = [university.strip() for university in universities]
        # for university in universities:
            # print(university)

    # # def parse(self, response):
    #     Country_names = response.xpath('//select[@id="Chp1"]/option/text()').getall()
        
        
    #     for index in range(1 , len(Country_names)):
    #         logging.debug(Country_names[index])
            
            
    #         self.request(Country_names[index])


        # yield {
        #     'Country Names ' : Country_names
        # }
        
      

# class WHEDSPIDER(scrapy.Spider):
#     name = 'World_higher_education_database'
#     institute_url = "https://www.whed.net/results_institutions.php"

#     payload = {
#         'Chp1': 'Afghanistan',
#         'Chp0': '',
#         'Chp2': '',
#         'Chp4': '',
#     }

#     cookies = {
#         'PHPSESSID': '9195bbb4ni1td1v4t2ulodhmte',
#     }





# cookie: PHPSESSID=9m4jgevdjs5use1kdg93aona59; 
# accepte_cookie=1; 
# accord_cookie=YES; __utma=71503701.53842636.1661162936.1661162936.1661162936.1; __utmc=71503701; __utmz=71503701.1661162936.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=71503701.16.10.1661162936
# origin: https://www.whed.net
# referer: https://www.whed.net/results_institutions.php
# sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "Linux"
# sec-fetch-dest: document
# sec-fetch-mode: navigate
# sec-fetch-site: same-origin
# sec-fetch-user: ?1
# upgrade-insecure-requests: 1
# user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36

#     def start_requests(self):
#         # scrapy.Request(url=self.institute_url, callback=self.parse_countries_names)
       
#         yield scrapy.FormRequest(
#             url=self.institute_url,
#             method="POST",
#             formdata=self.payload,
#             callback=self.parse,
#             cookies=self.cookies,
#             headers=self.headers
#         )

#     # def parse_countries_names(self,response):
#     #     print('In parsing functions')
#     #     logging.debug(response.body)
#     #     Country_names = response.xpath('//select[@id="Chp1"]/option/text()').getall()

#     #     yield {
#     #         'Counteries Names ' : Country_names
#     #     }

#     def parse(self, response):
#         universities = response.xpath('//*[@title="More details"]/text()').getall()
#         universities = [university.strip() for university in universities]
#         for university in universities:
#             print(university)
