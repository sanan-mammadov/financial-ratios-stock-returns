import pandas as pd

historical_data = pd.read_csv("historical_data.csv")

#Converting dates to datetime for proper filtering
historical_data['Date'] = pd.to_datetime(historical_data['Date'], format='%d-%m-%Y')

#Defining dates for quarter ends
quarter_end_dates = ['31-12-2015', '31-03-2016',
    '30-06-2016', '30-09-2016', '30-12-2016', '31-03-2017', '30-06-2017',
    '29-09-2017', '29-12-2017', '30-03-2018', '29-06-2018', '28-09-2018',                
    '31-12-2018', '29-03-2019', '28-06-2019', '30-09-2019', '31-12-2019',
    '31-03-2020', '30-06-2020', '30-09-2020', '31-12-2020', '31-03-2021',
    '30-06-2021', '30-09-2021', '31-12-2021', '31-03-2022', '30-06-2022',
    '30-09-2022', '30-12-2022', '31-03-2023', '27-06-2023', '29-09-2023',
    '29-12-2023'
]
quarter_end_dates = pd.to_datetime(quarter_end_dates, format='%d-%m-%Y')

#Filtering for these dates
filtered_data = historical_data[historical_data['Date'].isin(quarter_end_dates)]


quarterly_returns = []

#Grouping by stock symbol to calculate returns for each stock
for stock in filtered_data['Stock Symbol'].unique():
    stock_data = filtered_data[filtered_data['Stock Symbol'] == stock]
    stock_data = stock_data.sort_values(by='Date')

    for i in range(1, len(stock_data)):
        current_price = stock_data.iloc[i]['Close Price']
        previous_price = stock_data.iloc[i - 1]['Close Price']
        quarterly_return = (current_price - previous_price) / previous_price

        quarterly_returns.append({
            'Stock Symbol': stock,
            'Quarter': stock_data.iloc[i]['Date'],
            'Quarterly Return': quarterly_return
        })


returns_df = pd.DataFrame(quarterly_returns)
ret = returns_df['Quarterly Return']

returns_df.to_csv("quarterly_returns.csv", index=False)

financial_data = pd.read_csv("financial_ratios.csv")
financial_data['Quarterly Return'] = ret.values
#requied columns
required_columns = ['Stock Symbol', 'Quarter', 'Change in ROA (in %)','Change in ROE (in %)', 
                    'Change in Net Income Margin (in %)', 'Change in EBITDA Margin (in %)', 
                    'Change in Current Ratio', 'Change in Quick Ratio', 'Change in Cash Ratio', 
                    'Change in Debt-to-Equity','Quarterly Return']
financial_data = financial_data[required_columns]
financial_data.to_csv("final_data.csv", index=False) #final table
