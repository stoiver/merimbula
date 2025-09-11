import pandas as pd
import numpy as np

file_name = 'boundary.txt'

df = pd.read_csv(file_name, sep=r'[,\s]+', engine='python', names=['Day', 'Stage'])

naive_dt = pd.Timestamp('2004-09-30') # 274th day of 2004
localized = naive_dt.tz_localize('Australia/Sydney')

df['timestamp'] = np.round((df['Day'].values - 274)*3600*24 + (localized.value//10**9))
df['DateTimeTZ'] = pd.to_datetime(df['timestamp'], unit='s', utc=True).dt.tz_convert('Australia/Sydney')

df.to_csv('boundary.csv', index=False)
