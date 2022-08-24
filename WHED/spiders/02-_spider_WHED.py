from cmath import log
from curses import meta
from distutils.log import debug
from email import header
from wsgiref import headers
import math
import cupshelpers
import debian
from pkg_resources import yield_lines
from pytz import country_names
import scrapy
import requests
import logging
from scrapy import FormRequest
logging.basicConfig(filename="log_02.txt", level=logging.DEBUG)

class WHEDSPIDER(scrapy.Spider):
    break_page_conditon = 0
    CountryName = []
    UniversityName = []
    name = "World_higher_education_database"
    root_url = 'https://www.whed.net/results_institutions.php'
    
    Dataframe = []


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
            yield scrapy.Request(url=self.root_url, callback=self.get_counteries_names)
            print('back')


    def get_counteries_names(self,response):
        Country_names = response.xpath('//select[@id="Chp1"]/option/text()').getall()[1:]
        print(f'Country Names : {Country_names}')


        for index , country in enumerate( Country_names):

            # payload 
            payload = { 'Chp1': '',
                        'Chp0':'', 
                        'Chp2':'',
                        'Chp4': '',
                        'nbr_ref_pge': '100',
                        'debut' : '0'
                        }
            payload['Chp1']= country

            yield FormRequest(
                        url=self.root_url,
                        method="POST",
                        formdata=payload,
                        callback=self.get_page,
                        cookies=self.cookies,
                        headers=self.headers,
                        meta = {'temp_payload' :payload,
                                'nbr_ref_pge' : payload['nbr_ref_pge']}

                    )
            
        # yield {'Data' : self.Dataframe }
            break
        
            

 
    def get_page(self,response):
        Number_of_pages = len(response.xpath('//*[@id="contenu"]/div/div/a').getall())
        print(f'Number of pages {Number_of_pages}')
        
        temp_payload = response.meta['temp_payload'] 
        print(f'payload : {temp_payload}')
        country_name = response.meta['temp_payload']['Chp1']
        Number_of_refer_page = response.meta['temp_payload']['nbr_ref_pge']
        count = 0


        # page for each country
        
        for page in range(0,Number_of_pages+1):
           
            api = f'https://www.whed.net/results_institutions.php?Chp1={country_name}&Chp0=&Chp2=&Chp4=&nbr_ref_pge={Number_of_refer_page}&debut={count}'
            count += 100

            yield scrapy.Request(url=api, callback=self.get_universities ,meta = {'Country Name':country_name })


    def get_universities(self,response):
        
        Total_Universites_on_current_page = len(response.xpath('//*[@id="results"]/li'))

        
        for index in range(1, Total_Universites_on_current_page+1):
            X_Path_Universites_Name = f'//*[@id="results"]/li[{index}]/div[2]/h3/a/text()'
            X_Path_university_url = f'//*[@id="results"]/li[{index}]/div[2]/h3/a/@href'
            University_Name = response.xpath(X_Path_Universites_Name).get().strip()
            university_link = 'https://www.whed.net/'+str(response.xpath(X_Path_university_url).get())
            country_name = response.meta['Country Name']
            
            
            level_1 = {country_name : [
                                        { 'University_Name': University_Name , 
                                        'Univesity_rul' : response.url}
            ]}

            self.Dataframe.append(level_1)
           


            # yield {
            #     'Country' : country_name,
            #     'Univesitsity Name ' : University_Name,
            #     'University_url' : university_link
            # }

            yield scrapy.Request(url=university_link, callback=self.get_school_name_and_field_of_study ,meta = {'Country' : country_name,
                                                                                                    'Univesitsity_Name' : University_Name,
                                                                                                    'University_url' : university_link})

    def get_school_name_and_field_of_study(self,response):
        
        
        Enginnering_tag = ['engineering'] 
        IT_tag = ['Computer science' ,'software Engineering' ,'information Technology']
        
        
       
        # for department 
      
        for heading in response.css('h3'):
            if heading.css('::text').get('').strip() == 'Divisions':
                division = heading.xpath('following-sibling::div[@class="dl"]')[0]
                division = division.css('p.principal::text')
                print(division.getall())
                Department = division.getall()


        # for field of study
        for heading in response.css('h3'):
            if heading.css('::text').get('').strip() == 'Divisions':
                division = heading.xpath('following-sibling::div[@class="dl"]')[0]
                division = division.css('span.contenu::text')

                field_of_study = division.getall()

        # comparing cerateria
        School = []
        for index1, field in enumerate(field_of_study):
            temp_field = field.split(',') # split at , for comparing
            for name in temp_field:
                if name.lower() in Enginnering_tag or IT_tag:
                    
                    School.append(
                                {'School' :Department[index1] ,
                                'Field of Study' : field_of_study[index1] 
                                }
                            
                    )
                    break
        print(School)
        print(len(Department) == len(field_of_study))

        
        # logging.debug('Department : ',department)
        # logging.debug('Field of study : ',field_of_study)
        




        yield {
                'Country' : response.meta['Country'],
                'Univesitsity Name ' :  response.meta['Univesitsity_Name'],
                'University_url' :  response.meta['University_url'],
                # 'Department' : department,
                # 'Field_of_study' : field_of_study,
                'School' : School 
        }