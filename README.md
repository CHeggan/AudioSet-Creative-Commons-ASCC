# AudioSet-Creative-Commons-ASCC

A raw sample data release of the creative commons samples in the AudioSet ontology. The dataset and code to do create it is free to use for research and educational purposes.

## About AudioSet
Released by Google in 2017, the AudioSet ontology consists of 632 hierarchically structured audio event classes spanning 2,084,320 10-second long samples. Unfortunately, the raw data samples for the dataset are not readily available for download. Instead the data has been pre-feature-extracted using Google's own VGG-ish network, the output for which is a 128-dimensional feature vector for every second of a given sample(1Hz). 

## Sample Licensing
For YouTube videos, there appear to be 2 primary categories for licensing:
 - Creative Commons (Can use freely)
 - Non-Specified/ Standard YouTube License (cannot be reproduced or distributed in any other form without your consent)
 
Although every video has a license, it is very common for a scrape attempt to not retrieve anything. In our runs, we found that ~10-15% of videos had an unobtainable license file. We assume that these videos have the standard YouTube license to avoid issues.

### Benefits of Creative Commons
The main benefit of creative commons, especially for those who work heavily in open source or research is the ability to redistribute the data without legal implication. This means that the dataset provided here can be reuploaded/shared elsewhere, allowing for more reproducibility. 

## Dataset Details & Download
This dataset contains a total of 10789 audio samples, each 10s long. All files were downloaded late 2021 and so the full set will likely contain more samples that if it were to be downloaded today (random loss of videos on YouTube from the ontology). No particular focus was put on maintaining balance between classes (as it would have required undersampling some files we obtained). There are supplied multi-label labels from the original ontology, so this is still possible as an extra setup is needed. 

The full dataset along with labels can be downloaded from [Google Drive](https://drive.google.com/drive/folders/1f2Rw4o36FbMi5YOijz3JKoumhPW7slyd?usp=sharing).

## File Description
### Original MetaData Files
 - big_data.csv : Contains majority of the details for the full AudioSet ontology
 - labels.csv : mID to human-readable label conversion
 - ontology.json : Heirarchy information
 - qa_true_counts.csv : Estimated quality of class labelling
 - suitable_classes.npy : A numpy array containing all human readable classes and their mIDs which we are intererested in downloading from. We include all classes in AudioSet in this file to cover all possible files. How this file and suitable class selection works can be found [here]()

### Python Scripts
 - invest_1.py : Iterates through the 'big_data' dataframe and grabs the license for every single sample (outputs csv files which are combined into all_cc_df.csv)
 - cc_class_dist.py : Iterates through all found CC files and grabs all relevent yID/label pairings to maintain multi-label (outputs all_cc_qual_0_false.csv)
 - download_cc.py : Downloads all CC files (outputs main data folder with files)

### Generated Files
 - all_cc_df.csv : A collected of YIDs of all CC licensed vides found from search
 - all_cc_qual_0_false.csv : A collection of YID/MID(label) pairs. We do this so that we can later maintain the multi-label nature of the original dataset
 - label_df.csv : Final multi-label labels for the CC licensed files

## Citation
If you use this dataset in your research, please cite the paper it was created for use in:
[ICANN22 Link](https://link.springer.com/chapter/10.1007/978-3-031-15919-0_19#Ack1) or [arXiv Link](https://arxiv.org/pdf/2204.02121v2.pdf)
```
@InProceedings{10.1007/978-3-031-15919-0_19,
author="Heggan, Calum
and Budgett, Sam
and Hospedales, Timothy
and Yaghoobi, Mehrdad",
editor="Pimenidis, Elias
and Angelov, Plamen
and Jayne, Chrisina
and Papaleonidas, Antonios
and Aydin, Mehmet",
title="MetaAudio: A Few-Shot Audio Classification Benchmark",
booktitle="Artificial Neural Networks and Machine Learning -- ICANN 2022",
year="2022",
publisher="Springer International Publishing",
address="Cham",
pages="219--230",
isbn="978-3-031-15919-0"
}
