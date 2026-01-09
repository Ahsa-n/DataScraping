from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
driver = webdriver.Chrome()
driver.get("https://shop.tamimimarkets.com/")

# grab the actual category links in the carousel
catg= driver.find_elements(By.CSS_SELECTOR, ".carousel-wrapper .elements-div a")
categories = []
# exclude last 2
for cat in catg[:-2]:
    categories.append( cat.get_attribute("textContent"))
df = pd.DataFrame(columns=["ProductName", "Brand", "Price", "Link"])
print(df)
driver.get(f"https://shop.tamimimarkets.com/category/{categories[0].lower()}/")
driver.implicitly_wait(3)
time.sleep(3)  # let product grid render
height = driver.execute_script("return document.body.scrollHeight")
print(height)
products = []
brands = []
prices = []
links = []
x=0
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2.5)  # wait for page to load
    newheight = driver.execute_script("return document.body.scrollHeight")
    x+=1
    if newheight == height:
        break
    height = newheight
time.sleep(5)  # let product grid render
prodname = driver.find_elements(By.CSS_SELECTOR, ".Text-sc-1bsd7ul-0.Product__StyledNameText-sc-13egllk-16.bzHWnV")
for prod in prodname:
    products.append(prod.get_attribute("textContent"))
brandname = driver.find_elements(By.CSS_SELECTOR, ".Text-sc-1bsd7ul-0.ebqvdy")
for brand in brandname:
    brands.append(brand.get_attribute("textContent"))
price = driver.find_elements(By.CSS_SELECTOR, ".Text-sc-1bsd7ul-0.buIGqH")
for price in price:
    prices.append(price.get_attribute("textContent"))
link = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-collection'] a[href^='/product/']")
for a in link:
    links.append(a.get_attribute("href"))
print(len(products), len(brands), len(prices), len(links))
for i in range(len(products)-len(brands)):
    brands.append("N/A")
df = pd.DataFrame({"ProductName": products,
                   "Brand": brands,
                   "Price": prices,
                   "Link": links})
df.to_csv("tamimi_products.csv", index=False)