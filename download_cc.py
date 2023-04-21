"""
This script takes the creative commons (cc) id-label dataframe and attempts to 
    download all of the samples. 

Want to design it so that can operate in stop start mode as could be ~10k files, 
    in this manner, use:
        -> A hot loadable label dataframe to keep track of downloaded instances

"""
################################################################################
# IMPORTS
################################################################################
import os
import io
import sys
import ffmpy
import warnings
import youtube_dl
import numpy as np
import pandas as pd
import soundfile as sf
from tqdm import tqdm, trange

from contextlib import redirect_stdout, redirect_stderr

warnings.simplefilter(action='ignore', category=FutureWarning)

################################################################################
# HELPER FUNCTIONS
################################################################################
def create_directory(main_dataset_path):
    # Makes sure main data directoty is made
    try: 
        os.mkdir(main_dataset_path)
    except:
        print('Couldnt make main data folder')

    # Name of the folder main samples will be stored in
    sample_folder = os.path.join(main_dataset_path, 'Raw Samples')

    try:
        os.mkdir(sample_folder)
    except:
        print('Couldnt make sub sample data folder')

    return sample_folder

def add_label(label_df, id, num_id, all_classes, class_ids):#
    row = {}
    row['id'] = id
    row['num_id'] = num_id
    for cid in all_classes:
        if cid in class_ids:
            row[cid] = 1
        else:
            row[cid] = 0
    label_df = label_df.append(row, ignore_index=True)
    return label_df

################################################################################
# DOWNLOAD & FORMATTING
################################################################################
def download_audio(link, start, end, cookie_path):
    """
    Function responsible for actually downloading the file from youtube. This
        is mainly done through the youtube_dl library where options are used
        to only grab the audio.

    :param link: str
        The youtube compatible link for the file attempting to
            be downloaded

    :return filename: str
        The name of the file, a return of '0' indicates a
            download failure, anything else should be a success.
    """
    # Names the file straight away, if not changed by return, failure has occured
    filename='0'
    # Obtains a list of files in directory, important for later identifying download
    listdir=os.listdir()

    # Options for the downloading of file, in this case we want bets quality audio
    options = {
    'quiet': True, # Mutes normal output
    'no-warnings': True, #Mutes warnings
    'ignore-errors': True, # Ignores errors, i.e exceptions etc
    'format': 'bestaudio/best', # Downloads the best quality audio
    'extractaudio' : True,  # only keep the audio
    'noplaylist' : True,    # only download single song, not playlist
    }

    # if we have a cookie path we can use it
    if cookie_path != 'None':
        options['cookiefile'] = cookie_path # Path to the cookies file


    # The code here uses try to avoid a crash when rare downloads inevitably fail
    try:
        f = io.StringIO()
        with redirect_stdout(f), redirect_stderr(f):
            youtube_dl.YoutubeDL(options).download([link])

        # Comapres new to old directory file lists to find the new file
        listdir2=os.listdir()
        for i, val in enumerate(listdir2):
            if listdir2[i] not in listdir:
                filename=listdir2[i]
                break

        # want to check the length of the file so that we dont have smaples< 10s
        length = youtube_dl.YoutubeDL(options).extract_info(link)['duration']
        # Files that are excatly 10s typically get shortened by a second, so 11s needed
        if  length < 10:
            os.remove(filename)
            filename='0'
        # Wierd start/ends have been selected for some files so have to sort this
        if end >= length:
            os.remove(filename)
            filename='0'

        if end-start != 10:
            os.remove(filename)
            filename ='0'


    # Skips forward if try function fails, indicating the fle cannot be retrieved
    except Exception:
        filename ='0'

    return filename

def file_cleaning(filename, start, end, yid, num_id, defaultdir):
    """
    This function cleans/clips teh downloaded audio clip to the specific 10s range
        that describes the clas in question. Also converts the file to .wav and
        renames it so the class datasets are more cohesive in naming convention.

    :param filename: str
        The current name of the file as given by download function
    :param start: int 
        Start time in seconds of the class clip form raw file
    :param end: int 
        End time in seconds of the class clip form raw file
    :param defaultdir: str 
        The base directory of the full codeset, i.e '...\AudioSet',
            this is needed to point to the ffmpeg.exe file used for conversion


    :return filename: str 
        The new name of the file with the numbering convention
    :return samplerate: int
        The samplerate determined by soundfile library, is returned
            so that it can be noted in saved example data

    :save: .wav file
        Saves the recently downloaded file under a new name after clipping to
            the 10s example
    """
    # Grabs the extension from the file name
    extension = os.path.splitext(filename)[1]
    begin_file = os.path.splitext(filename)[0]

    # Renames the file with num of sample/ start and end times
    os.rename(filename,'%s%s'%(num_id, extension))

    # Redefines new filenames
    filename='%s%s'%(num_id, extension)

    # If the file type isnt already .wav, we want to change it to be
    if extension not in ['.wav']:
        xindex = filename.find(extension)
        filename = filename[0 : xindex]

        # Uses the executable ffmpeg file to run audio conversion, needs default directory
        ff = ffmpy.FFmpeg(executable = defaultdir + '\\ffmpeg.exe',
            global_options = ('-hide_banner -loglevel panic -nostats'),
            inputs = {filename + extension:None},
            outputs = {filename +'.wav':None},
            )
        ff.run()
        os.remove(filename+extension)

    # Uses information of the audio sample to cut it down to the 10s interval specified in metadata
    file = filename+'.wav'
    data, samplerate = sf.read(file)
    totalframes = len(data)
    totalseconds = totalframes / samplerate
    startsec = start
    startframe = samplerate * startsec
    endsec = end
    endframe = samplerate * endsec

    # Writes the newly cut down file
    os.remove(file)
    sf.write(file, data[int(startframe):int(endframe)], samplerate)

    return file, samplerate

################################################################################
# MAIN FUNCTION
################################################################################
def main(main_dataset_path, df_name):
    # Loads in the cc dataframe with id-label pairs
    cc_df = pd.read_csv(df_name + '.csv')
    classes = list(cc_df['class_id'].unique())

    # Deals with the import of big_data.csv, created in compile_data.py
    big_data = pd.read_csv('big_data.csv', index_col=0)
    # YouTube ID(col1) has to be changed so we can do a comparison on columns later on
    big_data = big_data.rename(columns={"0": "YID"})
    
    # Create and returns teh path for the sample containing folder
    sample_folder = create_directory(main_dataset_path)

    label_df_name = 'label_df.csv'

    # Tries to load a current label dataframe, makes a new one if cannot
    try: 
        label_df = pd.read_csv(label_df_name, index_col=0)
    except:
        print('Creating a fresh label dataframe')
        # Generates a blank 
        label_columns = ['id'] + ['num_id'] + classes
        label_df = pd.DataFrame(columns=label_columns)

    ids = cc_df['id'].unique()
    main_loop = tqdm(enumerate(ids), total=len(ids))

    slink = 'https://www.youtube.com/watch?v='

    yid_complete = label_df['id'].unique()

    for idx, yid in main_loop:

        # If have already completed yid, we skip over
        if yid in yid_complete:
            continue
        
        # Grabs relevant meta data for YID from large collection
        meta_data = big_data[big_data['YID']== yid]

        # Creates the youtube link used for actually downloading
        yid = meta_data.iloc[0, 0]
        link = slink + yid

        # Additional meta data retrival
        start = meta_data.iloc[0, 1]
        end = meta_data.iloc[0, 2]

        os.chdir(sample_folder)

        filename = download_audio(link, start, end, None)

        # if file errors then we skip
        if filename == '0':
            continue

        # Formats the file, i.e trims etc
        new_filename, sr = file_cleaning(filename, start, end, yid, idx, main_dataset_path)

        sub_cc_yid = cc_df[cc_df['id'] == yid]

        needed_ids = sub_cc_yid['class_id'].unique()

        # Add out new row to teh dataframe
        label_df = add_label(label_df, yid, idx, classes, needed_ids)

        os.chdir(main_dataset_path)

        label_df.to_csv(label_df_name)

        main_loop.update(1)

path = 'X:/Datasets/CC_AudioSet'
main(path, 'all_cc_qual_0_false')