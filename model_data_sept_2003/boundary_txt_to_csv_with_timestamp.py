import pandas as pd
import numpy as np

file_name = 'boundary.txt'

df = pd.read_csv(file_name, sep=r'[,\s]+', engine='python', names=['Day', 'Stage'])


naive_dt = pd.Timestamp('2003-09-22') # 265th day of 2003
localized = naive_dt.tz_localize('Australia/Sydney')

df['timestamp'] = np.round((df['Day'].values - 265)*3600*24 + (localized.value//10**9))
df['DateTimeTZ'] = pd.to_datetime(df['timestamp'], unit='s', utc=True).dt.tz_convert('Australia/Sydney')

df.to_csv('boundary.csv', index=False)
