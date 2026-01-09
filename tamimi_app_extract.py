import json
import pandas as pd
import openpyxl
with open('tamimi_home_page.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
# variants = 0
products = data["data"]["page"]["layouts"][4]["value"]["collection"]["product"]
# for x in range(len(products)):
#     variants +=  len(products[x]["variants"]) #number of posssible rows
# print(variants) # for csv row based for each product

# for csv column based for each variant
df = pd.DataFrame(columns=["Product Name", "Brand", "Original Price","Discounted Price","Stock"])
for product in products:
    variant = product["variants"]
    for v in variant:
        specific = v["storeSpecificData"]
        for s in specific:
            df.loc[len(df)] = [v["fullName"], product["brand"]["name"], s["mrp"], float(s["mrp"]) - float(s["discount"]), s["stock"]]
print(df)       
df.to_csv('products.csv', index=False)
df.to_excel('products.xlsx', index=False)
