import os
import time
import subprocess
import youtube_dl
import pandas as pd
from tqdm import tqdm


meta_path = 'big_data.csv'

meta_df = pd.read_csv(meta_path)
all_ids = meta_df.iloc[:,1].values

link = 'https://www.youtube.com/watch?v='

cc = 0
nas = 0
errored = 0
total_covered = 0

id_dict_list = []

start_idx = 0 #40001
end_idx = 10

start = time.time()
for yid in all_ids[start_idx:end_idx]:
    new_link = link + str(yid)
    command = "youtube-dl --get-filename -o '%(license)s' " + str(new_link)

    try:
        x = str(subprocess.check_output(command, shell=True))
        x_arr = x.split("'")
        license = x_arr[1]
        print(license)
        if license == 'Creative Commons Attribution license (reuse allowed)':
            cc += 1
        elif license == 'NA':
            nas += 1

        id_dict_list.append( {'id':yid, 'license':license} )

    except:
        errored += 1
        #print('CANNOT RETRIEVE')

    total_covered += 1

end = time.time()

print('\n')
print(f'Time Taken: {end-start}')
print(f'Covered: {total_covered}')
print(f'Errored: {errored}')
print(f'CC: {cc}')
print(f'NA: {nas}')

out_df = pd.DataFrame(id_dict_list)
out_str = 'licenses_' + str(start_idx) + '_' + str(end_idx)
out_df.to_csv(out_str + '.csv')


"""
#os.system("youtube-dl -o '%(title)s by %(uploader)s on %(upload_date)s in %(playlist)s.%(ext)s' https://www.youtube.com/watch?v=7E-cwdnsiow")
result = os.system("youtube-dl --get-filename -o '%(title)s.%(ext)s.%(license)s' ZNEPaGFApX4")
print(result)
"""
#x = subprocess.check_output("youtube-dl --get-filename -o '%(license)s' ZQ-mrOVK1Oo", shell=True)
#print(x)
