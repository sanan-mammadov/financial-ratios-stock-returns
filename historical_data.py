                    #Fetch Historical Data for Each Stock
import pandas as pd
import requests
stock_list = ['VESTL', 'DITAS', 'TMSN', 'ULUSE', 'GEREL', 'TTRAK', 'KARSN',
              'TOASO', 'SILVR', 'FROTO', 'PARSN', 'ALCAR', 'MAKTK', 'ASUZU',
              'SAYAS', 'PRKAB', 'BFREN', 'JANTS', 'EGEEN', 'BNTAS', 'OTKAR',
              'KLMSN', 'ARCLK', 'IHEVA', 'EMKEL', 'VESBE', 'KATMR']
def fetch_historical_data(stock_symbol):
    url = f"https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse={stock_symbol}&startdate=01-12-2015&enddate=01-01-2024"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            historical_data = response.json()['value']
            df = pd.DataFrame(historical_data)
            return df
        except KeyError:
            print(f"Key 'value' not found in the response for {stock_symbol}. Full response: {response.json()}")
            return None
    else:
        print(f"Failed to fetch data for {stock_symbol}, status code: {response.status_code}")
        return None


historical_data_list = {}
for stock in stock_list:
    historical_data = fetch_historical_data(stock)
    if historical_data is not None:
        historical_data_list[stock] = historical_data
        print(f"Data fetched for {stock}.")



historical_data_list_df = pd.concat(historical_data_list, keys=historical_data_list.keys())
#renaming
historical_data_list_df = historical_data_list_df.rename(columns={"HGDG_HS_KODU": "Stock Symbol", "HGDG_TARIH": "Date", "HG_KAPANIS": "Close Price"})

required_columns = ['Stock Symbol', 'Date', 'Close Price']
historical_data_list_df = historical_data_list_df[required_columns]
historical_data_list_df.to_csv("historical_data.csv", index=False)

