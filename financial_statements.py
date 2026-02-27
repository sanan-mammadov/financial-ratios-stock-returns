import pandas as pd
import requests

url = "https://finans.mynet.com/borsa/endeks/xmesy-bist-metal-esya-makina/endekshisseleri/"
tables = pd.read_html(url)

bist_manufacture = tables[0]
bist_manufacture.columns = ['Hisseler', 'Unnamed: 1', 'Son', 'Değişim Yüzde', 'Hacim (TL)', 'Saat']
bist_manufacture['Stock Symbol'] = bist_manufacture['Hisseler'].str.split().str[0]
bist_manufacture = bist_manufacture.drop(columns=['Hisseler', 'Unnamed: 1'])

#Getting the stock symbols
stock_list = bist_manufacture['Stock Symbol']


def fetch_financial_data_by_year(stock_symbol, year):
    """
    Fetch financial data for a specific stock and year.
    """
    url = (
        f"https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
        f"?companyCode={stock_symbol}&exchange=TRY&financialGroup=XI_29"
        f"&year1={year}&period1=12&year2={year}&period2=9"
        f"&year3={year}&period3=6&year4={year}&period4=3"
    )
    
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return pd.DataFrame(response.json()['value'])
        except KeyError:
            print(f"No data available for {stock_symbol} in year {year}.")
            return pd.DataFrame()
    else:
        print(f"Failed to fetch data for {stock_symbol} in year {year}, Status Code: {response.status_code}")
        return pd.DataFrame()


def rename_columns_by_year(data, year):
    """
    Renaming value columns to include year and quarter.
    """
    if not data.empty:
        quarter_mapping = {
            'value1': f'{year}_Q4',
            'value2': f'{year}_Q3',
            'value3': f'{year}_Q2',
            'value4': f'{year}_Q1'
        }
        data = data.rename(columns=quarter_mapping)
    return data


def fetch_and_combine_data(stock_symbol, start_year, num_years):
    """
    Fetching and combining financial data for a specific stock over multiple years.
    """
    combined_data = pd.DataFrame()
    
    try:
        for year in range(start_year, start_year - num_years, -1):
            print(f"Fetching data for {stock_symbol} in year {year}...")
            yearly_data = fetch_financial_data_by_year(stock_symbol, year)
            yearly_data = rename_columns_by_year(yearly_data, year)
            
            if combined_data.empty:
                combined_data = yearly_data
            else:
                combined_data = pd.merge(combined_data, yearly_data, on=['itemCode', 'itemDescTr', 'itemDescEng'], how='outer')
    except Exception as e:
        print(f"Error processing data for {stock_symbol}: {e}")
        return pd.DataFrame()

    return combined_data


def fetch_all_stocks_data(stock_list, start_year, num_years):
    """
    Fetching and combining financial data for all stocks in the stock list.
    Skip stocks with errors.
    """
    combined_data = pd.DataFrame()

    for stock in stock_list:
        print(f"Fetching data for {stock}...")
        stock_data = fetch_and_combine_data(stock, start_year, num_years)

        if not stock_data.empty:
            #Add a column to indicate the stock symbol
            stock_data['Stock Symbol'] = stock
            combined_data = pd.concat([combined_data, stock_data], ignore_index=True)
        else:
            print(f"Skipping {stock} due to errors or no data.")

    return combined_data


start_year = 2023 #Starting year for fetching data
num_years = 9 #Number of years to fetch data after the starting year

#Fetching data for all stocks
#Could give errors if website is down
full_data = fetch_all_stocks_data(stock_list, start_year=start_year, num_years=num_years) 

#Identify quarterly columns
quarter_columns = [col for col in full_data.columns if '_Q' in col and col not in ['2015_Q1', '2015_Q2', '2015_Q3']]

#Checking for missing values in quarter columns
print(f"Missing values in quarterly columns: {full_data[quarter_columns].isnull().sum()}")


#Dropping rows with NaN in quarterly columns only
data_cleaned = full_data.dropna(subset=quarter_columns)

print(f"Original dataset shape: {full_data.shape}")
print(f"Cleaned dataset shape: {data_cleaned.shape}")
#Getting only required columns
required_columns = ['Stock Symbol', 'itemCode', 'itemDescTr', 'itemDescEng'] + quarter_columns
data_cleaned = data_cleaned[required_columns]
data_cleaned.to_csv("financial_statements.csv", index=False) #27 stocks from manufacturing industry

data_cleaned["Stock Symbol"].unique() 
