import pandas as pd
from datetime import date
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as wait
import uuid
import time

# get the brand list
df_brand = pd.read_csv(r'brandlist.csv')

# get the category list
df_cat = pd.read_csv(r'category.csv')

####################################
##### online store - PARKnSHOP #####
####################################

name_list = []
brand_list = []
origin_list = []
quantity_list = []
original_price_list = []
discount_price_list = []
review_list = []
emarket_id = []
category = []
x = 0 # count the loop
driver = webdriver.Chrome('./chromedriver')

url = "https://www.pns.hk/zh-hk/"
try:
   driver.get(url)
except:
   print('url not found')
   exit
time.sleep(2)
meun_button = driver.find_element(By.XPATH, "/html/body/app-root/cx-storefront/header/cx-page-layout[2]/cx-page-slot[2]/pns-header-navigation-tab[1]/a")
hover = ActionChains(driver).move_to_element(meun_button).perform()
time.sleep(5)
categories = driver.find_elements(By.XPATH,'//div[@class="nav-subMenu-lv1"]/ul/li/a[@class="subCategorylv1"]')
category_list = []
for href in categories:
    category_list.append(href.get_attribute('href'))

# get the data of foods and beverage   
category_list.pop(2)
category_list.pop(7)
category_list.pop(4)
category_list.pop(-1)
for link in category_list:

    try:
        driver.get(link)
        time.sleep(2)
    except:
        print('category not found')
        exit
    try:
        show_all_button = driver.find_element(By.XPATH, '//div[@class="toggleAllBtn"]').click()
    except:
        exit
    sub_categories = driver.find_elements(By.XPATH,'//a[@class="category"]')
    sub_category_list = []
    for href1 in sub_categories:
        sub_category_list.append(href1.get_attribute('href'))
    for link1 in sub_category_list[:1]: # find 2 sub category
        try:
            driver.get(link1)
            time.sleep(2)
        except:
            print('sub_category not found')
            exit
        sub_category_name = driver.find_element(By.XPATH,'//h1[@class="group-title"]').text
        if "/" in sub_category_name:
            sub_category_name = sub_category_name.replace("/"," ")
        SCROLL_PAUSE_TIME = 10
        last_height = driver.execute_script("return document.body.scrollHeight")
        print(last_height)
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        items = driver.find_elements(By.XPATH,'//a[@class="productName"]')
        item_list = []
        for href2 in items:
            item_list.append(href2.get_attribute('href'))
        item_list = item_list[:2]#  find sub category first(3)items
        #name_list = []
        #brand_list = []
        #origin_list = []
        #quantity_list = []
        #original_price_list = []
        #discount_price_list = []
        #review_list = []
        for link2 in item_list:
            emarket_id.append("1")
            if link == category_list[0]:
                category.append('飲品、即沖飲品')
            if link == category_list[1]:
                category.append('酒類、酒精飲品')
            if link == category_list[2]:
                category.append('米、麵、油、烘焙')
            if link == category_list[3]:
                category.append('罐頭、醃製食品、乾貨')
            if link == category_list[4]:
                category.append('零食、餅乾、甜品')
            if link == category_list[5]:
                category.append('冷凍、急凍食品')
            if link == category_list[6]:
                category.append('早餐、果醬')
            try:
                driver.get(link2)
                time.sleep(2)
            except:
                print('item not found')
                exit
            try:
                item = driver.find_element(By.XPATH,'//h1[@class="product-name"]')
                name_list.append(item.text)
            except:
                item_list.append("N/A")
            try:
                brand = driver.find_element(By.XPATH,'//div[@class="product-brand"]/a')
                brand_list.append(brand.text)
            except:
                brand_list.append("N/A")
            try:
                origin = driver.find_element(By.XPATH,'//div[@class="info-content"]')
                info_title = driver.find_element(By.XPATH,'//div[@class="info-title"]').text
                if info_title == "原產地":
                    origin_list.append(origin.text)
                else:
                    origin_list.append("N/A")
            except:
                origin_list.append("N/A")
            try:
                quantity = driver.find_element(By.XPATH,'//div[@class="product-unit"]')
                quantity_list.append(quantity.text)
            except:
                quantity_list.append("N/A")
            try:
                current_price = driver.find_element(By.XPATH,'//span[@class="currentPrice"]')
                original_price_list.append(current_price.text)
                discount_price_list.append("N/A")
            except:
                try:
                    original_price = driver.find_element(By.XPATH,'//span[@class="originalPrice"]')
                    original_price_list.append(original_price.text)
                    discount_price = driver.find_element(By.XPATH,'//span[@class="isDiscount currentPrice"]')
                    discount_price_list.append(discount_price.text)
                except:
                    original_price_list.append("N/A")
                    discount_price_list.append("N/A")
            SCROLL_PAUSE_TIME = 5
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            try:
                review = driver.find_element(By.XPATH,'//span[@class="score"]')
                review_list.append(review.text)
            except:
                review_list.append("N/A")
            time.sleep(2)
            print(name_list)
            print(brand_list)
            print(origin_list)
            print(quantity_list)
            print(original_price_list)
            print(discount_price_list)
            print(review_list)
            print(category)
            time.sleep(2)
            x = x+1
            print(x)
        
df = pd.DataFrame({'Product Name': name_list, 'Brand': brand_list,  'origin': origin_list,
                    'packing': quantity_list, 'Selling_Price': original_price_list, 'discounted_Price': discount_price_list,
                    'reviews': review_list,'emarket_id': emarket_id,'category':category, 'Date': date.today()})
        
print(df)
# add df brand id
df_add_brandid = df.merge(df_brand, on=['Brand'], how='left')
# add df category id
df_add_catid = df_add_brandid.merge(df_cat, on=['category'], how='left')
time.sleep(2)
df_add_catid['Selling_Price'] = df_add_catid['Selling_Price'].str.replace('$','')
df_add_catid['discounted_Price'] = df_add_catid['discounted_Price'].str.replace('$','')

##################################
##### online retailer - DKSH #####
##################################
name_list1 = []
brand_list1 = []
origin_list1 = []
price_list1 = []
category1 = []
emarket_id = []
y = 0
driver = webdriver.Chrome('./chromedriver')
url1 = "https://www.dchfoodmartdeluxe.com/te/index.php?lang=tc"
try:
   driver.get(url1)
except:
   print('url not found')
   exit
time.sleep(2)
try:
   close_button = driver.find_element(By.CLASS_NAME,"eupopup-closebutton").click()
except:
   exit
meun_button = driver.find_element(By.XPATH,'//*[@id="main-navbar"]/div/div[2]/div[2]/button').click()
time.sleep(2)
categories = driver.find_elements(By.XPATH,'//*[@id="main-menu"]/ul/li/a')
category_list = []
for href in categories:
    category_list.append(href.get_attribute('href'))
category_list.pop(12)
category_list.pop(9)

category_list = category_list[8:15]

for link in category_list:
    try:
        driver.get(link)
        time.sleep(2)
    except:
        print('category not found')
        exit
    sub_categories = driver.find_elements(By.XPATH,'//*[@id="content"]/div/div/section/div/div/div/span/div/a')
    sub_category_list = []
    for href1 in sub_categories:
        sub_category_list.append(href1.get_attribute('href'))
    sub_category_list = sub_category_list[1:]
    for link1 in sub_category_list:
        try:
            driver.get(link1)
            time.sleep(2)
        except:
            print('sub_category not found')
            exit
        items = driver.find_elements(By.XPATH,'//*[@id="content"]/div/div/section/div/div/div/div/a[@tabindex="-1"]')
        item_list = []
        for href2 in items:
            item_list.append(href2.get_attribute('href'))
        #name_list = []
        #brand_list = []
        #origin_list = []
        #price_list = []
        for link2 in item_list[:5]:
            emarket_id.append('2')
            try:
                driver.get(link2)
                time.sleep(2)
            except:
                print('item not found')
                exit
            item = driver.find_element(By.XPATH,'//*[@id="product_content"]/div/div/div/h1')
            name_list1.append(item.text)
            try:
                cat = driver.find_element(By.XPATH,'//div[@id="breadcrumb"]')
                cat1 = cat.text.split(' ')
                category1.append(cat1[2])
            except:
                category1.append("N/A")

            try:
                brand = driver.find_element(By.XPATH,'//span[contains(text(), "品牌:")]')
                brand = brand.text.split(': ')
                brand_list1.append(brand[1])
            except:
                brand_list1.append("N/A")
            try:
                origin = driver.find_element(By.XPATH,'//span[contains(text(), "產地:")]')
                origin = origin.text.split(': ')
                origin_list1.append(origin[1])
            except:
                origin_list1.append("N/A")
            price = driver.find_element(By.XPATH,'//*[@id="product_content"]/div/div/div/div/div')
            price = price.text.split(' ')
            price_list1.append(price[1]+price[2])
            time.sleep(2)
            y = y+1
            print(category1)
            print(name_list1)
            print(brand_list1)
            print(origin_list1)
            print(price_list1)
            print(y)

df_dch = pd.DataFrame({'Product Name': name_list1, 'Brand': brand_list1,
                       'origin': origin_list1, 'Selling_Price': price_list1,
                       'emarket_id': emarket_id,'category':category1,'Date': date.today()})
rep = {'急凍食品' : '冷凍、急凍食品',
'冷凍食品' : '冷凍、急凍食品',
'糧油雜貨' : '米、麵、油、烘焙',
'罐裝及包裝食品' : '罐頭、醃製食品、乾貨',
'各式飲品' : '飲品、即沖飲品',
'酒精飲品' : '酒類、酒精飲品',
'精選零食' : '零食、餅乾、甜品',
'素食煮意': '冷凍、急凍食品'}
df_dch['category'] = df_dch['category'].replace(rep)

#first little clean by python
df_dch['Selling_Price'] = df_dch['Selling_Price'].str.replace('$','')
def num(x):
  output = x.split('/')[0]
  return output

def num2(x):
  output = x.split('/')[1]
  return output

df_dch['unit'] = df_dch['Selling_Price'].apply(num2)
df_dch['Selling_Price'] = df_dch['Selling_Price'].apply(num)
df_dch['Selling_Price'] = df_dch['Selling_Price'].str.replace('$','')
df_dch['unit1']=df_dch['unit']
category_mapping = {'件': '1', '2件': '2', '3件':'3', '4件':'4', '8件': '8', '6件':'6','盒':'1'}
df_dch['unit1'] = df_dch['unit1'].replace(category_mapping)
df_dch['unit1']=pd.to_numeric(df_dch['unit1'])
df_dch['Selling_Price']=pd.to_numeric(df_dch['Selling_Price'])
df_dch['averageselling_perunit'] = df_dch['Selling_Price']/df_dch['unit1']
df_dch = df_dch.drop('unit1',axis=1)

# add df brand id
df_dch_add_brandid = df_dch.merge(df_brand, on=['Brand'], how='left')
# add df category id
df_dch_add_catid = df_dch_add_brandid.merge(df_cat, on=['category'], how='left')

dfcombine = pd.concat([df_add_catid,df_dch_add_catid],axis=0)
dfcombine.head(4)

#drop the non-meaningful columns
dfcombine = dfcombine.drop('Unnamed: 0_x',axis=1)
dfcombine = dfcombine.drop('Unnamed: 0.1',axis=1)
dfcombine = dfcombine.drop('Unnamed: 0_y',axis=1)

#prepare input to database need to drop brand and category to match the database table
dfcombine = dfcombine.drop('Brand',axis=1)
dfcombine = dfcombine.drop('category',axis=1)
#create a id to the product
dfcombine['product_id'] = [str(uuid.uuid4().int)[:9] for _ in range(len(dfcombine))]

dfcombine.to_csv(f'combine_{date.today()}.csv',mode='a',encoding="utf_8_sig")
driver.quit()
