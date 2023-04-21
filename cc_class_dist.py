import os
import sys
import numpy as np
import pandas as pd
from pandas.core.algorithms import unique




# Import sub_cc_df
sub_cc_df = pd.read_csv('all_cc_df.csv')
print(sub_cc_df.shape)
# Import big data
big_data = pd.read_csv('big_data.csv')

#print(big_data['0'])

suitable_classes = np.load('suitable_classes.npy')
labels = suitable_classes[:,0]
textlabels = suitable_classes[:,1]

print('Total Num Samples: {}'.format(len(sub_cc_df['id'].unique())))

pairs = []

num = 0


for idx, id in enumerate(sub_cc_df['id'].unique()):
    id_row = big_data[big_data['0'] == id]

    possible_classes = id_row.values[0][4:]

    for pos in possible_classes:
        if pos in labels:
            num += 1
            df_entry = {'id':id, 'class_id':pos}
            print(num, df_entry)
            pairs.append(df_entry)

new_df = pd.DataFrame(pairs)
new_df.to_csv('all_cc_qual_0_false_yo.csv')
