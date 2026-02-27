import pandas as pd


data = pd.read_csv("financial_statements.csv")

required_columns = ['Stock Symbol', 'itemCode', '2023_Q4', '2023_Q3', '2023_Q2', '2023_Q1', 
                    '2022_Q4', '2022_Q3', '2022_Q2', '2022_Q1', 
                    '2021_Q4', '2021_Q3', '2021_Q2', '2021_Q1', 
                    '2020_Q4', '2020_Q3', '2020_Q2', '2020_Q1', 
                    '2019_Q4', '2019_Q3', '2019_Q2', '2019_Q1',
                    '2018_Q4', '2018_Q3', '2018_Q2', '2018_Q1',
                    '2017_Q4', '2017_Q3', '2017_Q2', '2017_Q1',
                    '2016_Q4', '2016_Q3', '2016_Q2', '2016_Q1', '2015_Q4']
data = data[required_columns]

#Separate rows for each quarter
data_pivot = data.melt(id_vars=["Stock Symbol", "itemCode"], var_name="Quarter", value_name="Value")

final_table = pd.DataFrame()

#Calculating ratios and their changes
for stock_symbol in data_pivot['Stock Symbol'].unique():
    stock_data = data_pivot[data_pivot['Stock Symbol'] == stock_symbol]
    
    #Pivotting again to bring itemCode as columns where itemCode is the financial statement item code
    stock_data_pivot = stock_data.pivot(index="Quarter", columns="itemCode", values="Value").reset_index()

    if all(col in stock_data_pivot.columns for col in ['1A', '1AA', '1AF', '1B', '2A', '2B', '3L', '3CA', '1BL', '3DF', '3C', '2N', '4B']): #Columns required for calculations
        # Return on Assets (ROA)
        stock_data_pivot['ROA (in %)'] = (stock_data_pivot['3L'] / stock_data_pivot['1BL'])*100
        # Return on Equity (ROE)
        stock_data_pivot['ROE (in %)'] = (stock_data_pivot['3L'] / stock_data_pivot['2N'])*100
        # Net Profit Margin
        stock_data_pivot['Net Income Margin (in %)'] = (stock_data_pivot['3L'] / stock_data_pivot['3C'])*100
        # EBITDA Margin
        stock_data_pivot['EBITDA Margin (in %)'] = (stock_data_pivot['3DF'] + stock_data_pivot['4B']) / stock_data_pivot['3C']*100

        # Current Ratio
        stock_data_pivot['Current Ratio'] = stock_data_pivot['1A'] / stock_data_pivot['2A']
        # Quick Ratio
        stock_data_pivot['Quick Ratio'] = (stock_data_pivot['1A'] - stock_data_pivot['1AF']) / stock_data_pivot['2A']
        # Cash Ratio
        stock_data_pivot['Cash Ratio'] = stock_data_pivot['1AA'] / stock_data_pivot['2A']

        # Debt-to-Equity
        stock_data_pivot['Debt-to-Equity'] = (stock_data_pivot['2A'] + stock_data_pivot['2B']) / stock_data_pivot['2N']

        # Adding Stock Symbol
        stock_data_pivot['Stock Symbol'] = stock_symbol

        # Calculating changes in ratios
        stock_data_pivot = stock_data_pivot.sort_values('Quarter')  # Ensure data is sorted by Quarter
        stock_data_pivot['Change in ROA (in %)'] = stock_data_pivot['ROA (in %)'].diff() / stock_data_pivot['ROA (in %)'].shift(1)
        stock_data_pivot['Change in ROE (in %)'] = stock_data_pivot['ROE (in %)'].diff() / stock_data_pivot['ROE (in %)'].shift(1)
        stock_data_pivot['Change in Net Income Margin (in %)'] = stock_data_pivot['Net Income Margin (in %)'].diff() / stock_data_pivot['Net Income Margin (in %)'].shift(1)
        stock_data_pivot['Change in EBITDA Margin (in %)'] = stock_data_pivot['EBITDA Margin (in %)'].diff() / stock_data_pivot['EBITDA Margin (in %)'].shift(1)
        stock_data_pivot['Change in Current Ratio'] = stock_data_pivot['Current Ratio'].diff() / stock_data_pivot['Current Ratio'].shift(1)
        stock_data_pivot['Change in Quick Ratio'] = stock_data_pivot['Quick Ratio'].diff() / stock_data_pivot['Quick Ratio'].shift(1)
        stock_data_pivot['Change in Cash Ratio'] = stock_data_pivot['Cash Ratio'].diff() / stock_data_pivot['Cash Ratio'].shift(1)
        stock_data_pivot['Change in Debt-to-Equity'] = stock_data_pivot['Debt-to-Equity'].diff() / stock_data_pivot['Debt-to-Equity'].shift(1)

        final_table = pd.concat([final_table, stock_data_pivot], ignore_index=True)

#Reordering and selecting required columns
ordered_columns = [
    'Stock Symbol', 'Quarter', 
    'Change in ROA (in %)', 'ROA (in %)',
    'Change in ROE (in %)', 'ROE (in %)',
    'Change in Net Income Margin (in %)', 'Net Income Margin (in %)',
    'Change in EBITDA Margin (in %)', 'EBITDA Margin (in %)',
    'Change in Current Ratio', 'Current Ratio',
    'Change in Quick Ratio', 'Quick Ratio',
    'Change in Cash Ratio', 'Cash Ratio',
    'Change in Debt-to-Equity', 'Debt-to-Equity'
]
data_final = final_table[ordered_columns]

#Dropping null rows
data_final = data_final.dropna(axis=0)
#checking unique symbols
print(data_final.head())


data_final.to_csv("financial_ratios.csv", index=False)

#checking unique stocks
print(data_final["Stock Symbol"].unique()) #used in other files