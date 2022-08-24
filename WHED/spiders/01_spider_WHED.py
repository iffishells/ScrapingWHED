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
# logging.basicConfig(filename="log.txt", level=logging.DEBUG)

class WHEDSPIDER(scrapy.Spider):
    break_page_conditon = 0
    CountryName = []
    UniversityName = []
    name = "World_higher_education_database__"
    root_url = 'https://www.whed.net/results_institutions.php'
    payload = { 'Chp1': '',
                'Chp0':'', 
                'Chp2':'',
                'Chp4': '',
                'nbr_ref_pge': '100',
                'debut' : '0'
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
        count = 0
        for index in range(1 , len(Country_names)):
            
            self.payload['Chp1'] = Country_names[index]
            print(self.payload)
            
            # self.CountryName.append(Country_names[index])
            
            
        
            
            
            yield FormRequest(
                    url=self.root_url,
                    method="POST",
                    formdata=self.payload,
                    callback=self.parse_universites_name,
                    cookies=self.cookies,
                    headers=self.headers,
                    meta = {'Country_name' : Country_names[index]}

                )
            if index > 5:
                break
                
            
            
        
    def parse_page_handler(self,response):
        
        print(f'parse_page_handler function has been called')
        # payload = self.payload.copy()
        
        self.payload['debut'] = str(int(self.payload['debut']) + 100)
        print(f'payload {self.payload}')

        yield FormRequest(
                    url=self.root_url,
                    method="POST",
                    formdata=self.payload,
                    callback=self.parse_universites_name,
                    cookies=self.cookies,
                    headers=self.headers
                )




    def parse_universites_name(self,response ):
        # print(f'universities link of country : {response.url}')
        # logging.debug('this is response : ',response)
        
        All_Universites = int(response.xpath('//*[@id="contenu"]/form[2]/div/p/text()').get().split(' ')[-1])
        Total_Universites_on_current_page = len(response.xpath('//*[@id="results"]/li'))
        
        # Number_of_pages = len(response.xpath('//*[@id="contenu"]/div/div/a').getall())
        
        # print('Number of pages : ',Number_of_pages)
        # print('All Universites in current page : ',All_Universites)
        # print(f' Universites lenght {Total_Universites_on_current_page}')
  

        for index in range(1, Total_Universites_on_current_page+1):
            X_Path_Universites_Name = f'//*[@id="results"]/li[{index}]/div[2]/h3/a/text()'
            
            University_Name = response.xpath(X_Path_Universites_Name).get()
            self.break_page_conditon +=1
            count_name  = response.xpath('//*[@id="contenu"]/form[1]/p[2]/strong/text()').get().split('=')[1]

            print(f'Country Name  : {count_name} and University Name : {University_Name.strip()} and index : {index}')
            self.UniversityName.append(University_Name.strip())
            
                
            
        print(f'All Universites : {All_Universites}  and break condition : {self.break_page_conditon}')
        
        if All_Universites != self.break_page_conditon:
            print('Calling for more pages')
            print(f'payload {self.payload}')
            yield scrapy.Request(url = self.root_url , callback=self.parse_page_handler  ,dont_filter=True  )
        
        elif All_Universites == self.break_page_conditon:
            self.break_page_conditon=0
            self.payload['debut'] = '0'



