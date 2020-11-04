from flask import Flask, request
from flask_cors import CORS
from selenium import webdriver
import json
from selenium.common import exceptions 

app = Flask(__name__)
CORS(app)

listt = []
main_json = {}
def scrapping(keyword):


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome('.\chromedriver.exe',options=chrome_options)

    wd.get('https://www.shopclues.com/search?q='+keyword)
    #Scrapping
    results = wd.find_elements_by_class_name("search_blocks")
    link = wd.find_elements_by_css_selector('div.search_blocks a')
    image = wd.find_elements_by_css_selector('div.img_section img')
    
    final = []
    for item in range(len(results)):
        x = results[item].text
        items = x.split("\n")
        final.append(items)
    
    name = []
    price = []
    discount = []
    
    for item in final:
      for i in item:
        if '%' not in i and '₹' not in i:
          if 'shipping' not in i.lower():
            name.append(i)
        if '%' in i and '₹' in i:
          x = i.split(" ")
          price.append(x[0])
          discount.append(" ".join(x[1:]))


    for i in range(len(name)):
      details = {}
      details["Name"] = name[i]
      details["Price"] = price[i]
      details["Discount"] = discount[i]
      details["ImageSrc"] = image[i].get_attribute("src")
      details["NavLink"] = link[i].get_attribute("href")
      #print(details)
      listt.append(details)


    wd.get('https://www.croma.com/search/?text='+keyword)

    prod = wd.find_elements_by_class_name("product-title")
    amount = wd.find_elements_by_class_name("new-price")
    disc = wd.find_elements_by_class_name("discount")
    link = wd.find_elements_by_css_selector('h3.product-title a')
    image = wd.find_elements_by_css_selector('div.product-img img')

    discount = []
    for i in disc:
      if '%' in i.text:
        discount.append(i)

    name = []
    for i in prod:
      name.append(i)

    price = []
    for i in amount:
      price.append(i)

    
    for i in range(len(name)):
        details = {}
        details["Name"] = name[i].text
        details["Price"] = price[i].text
        details["Discount"] = discount[i].text
        details["ImageSrc"] = image[i].get_attribute("src")
        details["NavLink"] = link[i].get_attribute("href")
        #print(details)
        listt.append(details)
 

    wd.get('https://www.flipkart.com/search?q='+keyword)

    name = wd.find_elements_by_class_name("_3wU53n")
    price = wd.find_elements_by_class_name("_1vC4OE")
    link = wd.find_elements_by_css_selector('div._1UoZlX a')
    discount = wd.find_elements_by_class_name("VGWI6T")
    image = wd.find_elements_by_class_name("_1Nyybr")

    for i in range(len(name)):
        details = {}
        details["Name"] = name[i].text
        details["Price"] = price[i].text
        details["Discount"] = discount[i].text
        details["ImageSrc"] = image[i].get_attribute("src")
        details["NavLink"] = link[i].get_attribute("href")
        #print(details)
        listt.append(details)


    wd.get('https://paytmmall.com/shop/search?q='+keyword)

    name = wd.find_elements_by_class_name("UGUy")
    price = wd.find_elements_by_class_name("_1kMS")
    link = wd.find_elements_by_css_selector('div._3WhJ a')
    discount = wd.find_elements_by_class_name("c-ax")
    image = wd.find_elements_by_css_selector('div._3nWP img')

    results = wd.find_elements_by_class_name("_3WhJ")
    main = []
    for i in range(len(results)):
      main.append(results[i].text.split("\n"))
    #print(len(main))

    for item in range(len(main)):
      if "%" not in main[item][2]:
        discount.insert(item," ")

    for i in range(len(name)):
        details = {}
        details["Name"] = name[i].text
        details["Price"] = price[i].text
        if type(discount[i]) == str :
          details["Discount"] = discount[i]
        else:
          details["Discount"] = discount[i].text
        details["ImageSrc"] = image[i].get_attribute("src")
        details["NavLink"] = link[i].get_attribute("href")
        #print(details)
        listt.append(details)



@app.route('/search',methods = ['post'])
def hello():
    
    keyw = request.json['keyword']
    try: 
        scrapping(keyw)
    except exceptions.StaleElementReferenceException as e:
        print(e)
        pass  
    finally:
        main_json["Response"] = listt
        all_text = json.dumps(main_json)
        print(all_text)
        print(len(main_json))
        listt.clear()
    
    return all_text


if __name__ == '__main__':
   app.run(port=5000)