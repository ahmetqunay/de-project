#gerekli kutuphaneleri ice aktar
import pandas as pd
import numpy as np
import yfinance as yf
from pandas_datareader import data as pdr
from datetime import datetime
import json
from kafka import KafkaProducer
import time


#Yahoo Finance'dan finansal verileri cek
yf.pdr_override()

tech_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

#baslangic ve bitis tarihini belirt
end = datetime.now()
start = datetime(end.year - 10, end.month, end.day)

#her bir veriyi bir degisken olarak ata 
for stock in tech_list:
    globals()[stock] = yf.download(stock, start, end)
    


#Her bir sirketin verilerini iceren bir liste olustur
company_list = [AAPL, GOOG, MSFT, AMZN]
company_name = ["APPLE", "GOOGLE", "MICROSOFT", "AMAZON"]

#dataframe'e company_name adinda yeni bir kolon ekle
for company, com_name in zip(company_list, company_name):
    company["company_name"] = com_name

#verileri satir bazinda birlestir    
df = pd.concat(company_list, axis=0)
df.reset_index(inplace=True)

#tarihi formatla
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

# Float formatini duzenle
pd.options.display.float_format = '{:.2f}'.format

"""
#dataframe kolon isimlerini degistir
    df = df.rename(columns={
    "company_name": "firma",
    "Open": "acilis",
    "High": "en_yuksek",
    "Low": "en_dusuk",
    "Close": "kapanis",
    "Adj Close": "hacim",
    "Date": "tarih"
})

# CSV dosyasina kaydet
csv_filename = "tech_stocks.csv"
df.to_csv(csv_filename, index=False)
"""



#kafka yolunu ve topic adini belirt
server = "localhost:9092"
topic_name = "stocks2" #change

#verileri json formatina donustur
producer = KafkaProducer(
    bootstrap_servers = server,
    value_serializer = lambda x: json.dumps(x).encode("UTF-8")
)

#json formatina donusturulen her bir veriyi kafkaya gonder
for _, row in df.iterrows():
        to_json = row.to_dict()
        time.sleep(1)
        producer.send(f'{topic_name}',value= to_json)
        producer.flush()

producer.close()

