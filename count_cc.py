import os
import glob
import numpy as np
import pandas as pd 


csv_files = []
os.chdir("C:/Users/calum/OneDrive/PHD/2021/Code Base/Final AudioSet Repo Formatting/Licensing")
for file in glob.glob("csv_files/*.csv"):
    csv_files.append(file)

all_dfs = []

for file in csv_files:
    df = pd.read_csv(file)
    all_dfs.append(df)

big_df = pd.concat(all_dfs)

cc_df = big_df[big_df['license'] == 'Creative Commons Attribution license (reuse allowed)']

cc_df.to_csv('all_cc_df.csv')

print(f'CC Licenses: {len(cc_df)}')
print(cc_df['id'])

