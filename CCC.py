import requests
import pandas as pd
import csv

state_code = "MA"

city = "Boston"

loan_term = 30

interest_rate = 0.04

homes = []
homes2 = []
homes3 = []

url = "https://us-real-estate.p.rapidapi.com/for-sale"

querystring = {"offset":"0","limit":"200","state_code":state_code,"city":city,"sort":"price_min"}

headers = {
    'x-rapidapi-key': #rapid-api-key(confidential),
    'x-rapidapi-host': "us-real-estate.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

result = response.json()

listings = result["data"]["results"]

price = [listing["list_price"] for listing in listings]
prices = [float(0 if i is None else i) for i in price]

beds = [listing["description"]["beds"] for listing in listings]

baths = [listing["description"]["baths"] for listing in listings]

square_feet = [listing["description"]["sqft"] for listing in listings]

street_address = [listing["location"]["address"]["line"] for listing in listings]

postal_code = [listing["location"]["address"]["postal_code"] for listing in listings]

property_id = [listing["property_id"] for listing in listings]

for x in range(0, len(prices)):
    property_tax = ((0.0117) * (prices[x]))
    homes = [[prices[x]], [beds[x]], [baths[x]], [square_feet[x]], [street_address[x]], [postal_code[x]], property_tax, property_id[x]]
    homes2.append(homes)

def rent_estimater(bds, bths, sqft, zip, property_id):
    # some cool machine learning algorithm which calls getRent() from real estate api, in order to estimate reasonable rent
    return 5

def caprate_calculator(price, tax, rent):
    loan = (0.8 * price[0])
    yearly_principle = (loan / loan_term)
    yearly_interest = (loan * interest_rate)
    yearly_tax = float(tax)
    outflux = (yearly_interest + yearly_principle + yearly_tax)
    influx = float(rent)
    cashflow = (influx - outflux)
    caprate = (cashflow / price[0])
    return caprate

def call_rent1():
    url = "https://us-real-estate.p.rapidapi.com/for-rent"
    querystring = {"city":city,"state_code":state_code,"limit":"200","sort":"lowest_price"}
    headers = {
        'x-rapidapi-key': #rapid-api-key(confidential),
        'x-rapidapi-host': "us-real-estate.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return 10

def call_rent2():
    url = "https://us-real-estate.p.rapidapi.com/for-rent"
    querystring = {"city":city,"state_code":state_code,"limit":"200","sort":"highest_price"}
    headers = {
        'x-rapidapi-key': #rapid-api-key(confidential),
        'x-rapidapi-host': "us-real-estate.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    return 10
    
for x in range(0, len(homes2)):
    var = homes2[x]
    rent = rent_estimater(var[1], var[2], var[3], var[5], var[7])
    var.append(rent)
    cap_rate = caprate_calculator(var[0], var[6], rent)
    var.append(cap_rate)
    # down_payment = (0.2 * var[1])
    # var.append(down_payment)
    homes3.append(var)

print (homes3)

csvheader = ['List Price', 'Beds', 'Baths', 'sqft', 'Adress', 'Zip', 'Tax', 'Property ID', 'Rent', 'Cap Rate']

my_df = pd.DataFrame(homes3)
my_df.to_csv('did_it_work.csv', index=True, header=csvheader)
