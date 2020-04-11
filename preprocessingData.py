import csv
import pandas as pd

def read_data():
    with open('data/final.csv') as f:
        reader = csv.reader(f, delimiter=',')
        line = 0
        column = []
        data = []
        for row in reader:
            if line == 0:
                column = (row)
                line = line + 1
            else:
                data.append(row)

    return column[1:], data

def read_datapd():
    file = pd.read_csv('data/final.csv')
    file['Date'] = pd.to_datetime(file['Date'])
    return file

def sum_weekly_sale_by_week(df, idx = None):
    if idx == None:
        df_average_sales_week = df.groupby(by=['Date'], as_index=False)['Weekly_Sales'].sum()
        df_average_sales = df_average_sales_week.sort_values('Weekly_Sales', ascending=False)
        return df_average_sales_week
    else:
        df = df[df['Store'] == idx]
        df_average_sales_week = df.groupby(by=['Date'], as_index=False)['Weekly_Sales'].sum()
        df_average_sales = df_average_sales_week.sort_values('Weekly_Sales', ascending=False)
        return df_average_sales_week

def get_data(df, idx):
    return df[[df.Store == idx]]
