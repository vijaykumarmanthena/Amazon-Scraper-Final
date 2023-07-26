# Woring correctyly step 1 completed
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time as t
import json


import sys
import io

# Set stdout to use 'utf-8' encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"



driver=webdriver.Chrome()
#driver.maximize_window()
driver.get(url)


all_data=[]

def scrape():
    t.sleep(10)
    html=driver.page_source

    soup=bs(html,'html.parser')


    #print(html)
    """
    with open('amazon.html','w',encoding='utf-8') as f:
        f.write(html)"""

    all_divs=soup.find_all('div',{'class':'a-section a-spacing-small a-spacing-top-small'})

    print(len(all_divs))


    

    for i in all_divs[1:]:
        try:     
            #print(i.text)
            product_url=i.find('a',{'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
            product_name=i.find('a',{'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).span.text
            product=i.find('a',{'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
            product_price=i.find('span',{'class':'a-price'}).text#.span.extract().text
            #product_rating=i.find('i',{'class':'a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom'})#.span.extract().text  a-icon a-icon-star-small
            #product_rating=i.find('a',{'class':'a-popover-trigger a-declarative'})
            product_rating=i.find('span',{'class':'a-icon-alt'}).text
            num_of_reviews=i.find('span',{'class':'a-size-base s-underline-text'}).text
            
            middle=len(product_price)//2
            product_price=product_price[middle:]
            product_url=product_url if product_url else None
            product_name=product_name if product_name else None
            product_price=product_price if product_price else None
            product_rating=product_rating if product_rating else None
            num_of_reviews=num_of_reviews if num_of_reviews else None

           
            print(f"\nProduct url: {product_url}")
            print(f"\nProduct Name: {product_name}")
            print(f"\nProduct Price: {product_price}")
            print(f"\nProduct rating: {product_rating}")
            print(f"\nProduct Reviews: {num_of_reviews}")

            
            driver.refresh()
            driver.get(f"https://www.amazon.in/{product_url}")
            t.sleep(10)
            html2=driver.page_source
            soup2=bs(html2,'html.parser')
            product_features=soup2.find('div',{'id':'feature-bullets'})
            features=product_features.ul.find_all("li")
            features_list=[feature.text for feature in features]

            product_description=soup2.find("ul",{'class':'a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list'})#detailBullets_feature_div

            if product_description!=None:

                

                product_description_list=[product_description_item.text.replace('\n                                    \u200f\n                                        ','').replace("\n                                    \u200e\n                                 ",'')
                                        for product_description_item in product_description]
                
                product_description_list=[product_description_line.strip() for product_description_line in product_description_list if not (product_description_line==' ')]
                
                #product_description_list=[ product_description_line.split(':') for product_description_line in product_description_list]

                product_description_list={product_description_line.split(':')[0]:product_description_line.split(':')[1] for product_description_line in product_description_list}


                print("Openning product url")

                print("Description:\n")
                print(features_list)
                print("\n")
                print("Product Decription\n")
                print(product_description_list)
                print(f"\nASIN :{product_description_list['ASIN']}")
                print(f"\nManufacturer :{product_description_list['Manufacturer']}")

                data={"Product Url":f'https://www.amazon.in/{product_url}',"Product Name":f'{product_name}',"Product Price":product_price,"Product Rating":product_rating,"Product Reviews Count":num_of_reviews,"Description":features_list,"ASIN":product_description_list['ASIN'],"Product Description":product_description_list,"Manufacturer":product_description_list['Manufacturer']}
                all_data.append(data)

                #@upaated add all data

                print("\n")
                t.sleep(10)
 
        except Exception as e:
            print("Error")
            print(e)
            pass



scrape()

driver.get(url)
next=driver.find_element(By.LINK_TEXT,'Next')

#t.sleep(10)
url=driver.current_url
cnt=0
while(next):
    next.click()

    scrape()
    break
    next=driver.find_element(By.LINK_TEXT,'Next')
    cnt+=1
    if cnt==1:
        break
    
  

print("\n\n\nClosing the driver")
driver.close()

#print(all_data)


df=pd.DataFrame(all_data)

# ... Your existing code ...

# Convert the entire DataFrame to 'utf-8' encoding before saving to the Excel file
df = df.applymap(lambda x: x.encode('utf-8').decode('utf-8') if isinstance(x, str) else x)

# Save the DataFrame to an Excel file
df.to_excel("amazon_full.xlsx")

# ... Your existing code ...

print(df)

print(all_data)