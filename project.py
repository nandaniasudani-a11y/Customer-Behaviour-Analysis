import numpy as np
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+mysqlconnector://root:1111@127.0.0.1:3306/SALES_ANALYSIS"
)



print("Data uploaded successfully!")

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="your password",
    database="SALES_ANALYSIS"
)

cursor = conn.cursor()
data = pd.read_csv("youtube_project/dataset.csv")
# print(data.head())
# print(data.isna().sum())
# print(data["Category"])
# x=data.groupby("Category")["Review Rating"].median()
# print(x)
data["Review Rating"]=data["Review Rating"].fillna(data.groupby("Category")["Review Rating"].transform("median"))
# print(data.isna().sum())
data.columns=data.columns.str.lower()
data.columns=data.columns.str.replace(" ","_")
# print(data.columns)
data=data.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
# print(data.columns)

labels=["young","young-adult","adult","senior"]
data["age_group"]=pd.qcut(data['age'],q=4,labels=labels)
# print(data[["age","age_group"]].head())
print(data['frequency_of_purchases'].unique())

fre_map={ 'Fortnightly':14,         'Weekly':7,       'Annually':365,      'Quarterly':90,
      'Bi-Weekly':7,        'Monthly':30, 'Every 3 Months':90}

data['frequency_days']=data['frequency_of_purchases'].map(fre_map)
print(data[['frequency_of_purchases','frequency_days']].head())
data=data.drop('promo_code_used',axis=1)
print(data.columns)

data.to_sql(
    name="SALES",
    con=engine,
    if_exists="replace",
    index=False
)
