import pandas as pd
import numpy as np

file_name = 'Eden_tide_Sept03.dat'

df = pd.read_csv(file_name, sep=r'[,\s]+', engine='python', names=['Date', 'Time', 'Stage', 'Xmom', 'Ymom'])
df['DateTime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), dayfirst=True, format='%d/%m/%y %H:%M:%S')
df['DateTime'] = df['DateTime'].dt.tz_localize('Australia/Sydney')

df['timestamp'] = df['DateTime'].values.astype(np.int64) // 10**9

df.to_csv('Eden_tide_Sept03.csv')
