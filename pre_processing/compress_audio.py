"""
Utility script to rechannel and resample mp3 files in batch, with a nice
CLI and TQDM progress bar
"""

import torch
from torch.utils.data import Dataset

import torchaudio
import torchaudio.transforms

import sys, os

from pprint import pprint

from tqdm import tqdm

import json

import numpy as np

import matplotlib.pylab as plt
import seaborn as sns

import librosa
import librosa.display

import pandas as pd

from pathlib import Path

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
  "-g", "--genres", help="List of genres to compress", nargs='+', default=[]
)
parser.add_argument(
  "-c", "--channels", help="Number of audio channels", default=2
)

parser.add_argument(
  "-r", "--sample-rate", help="Sample rate in kHz", default=44100
)
args = parser.parse_args()

DATASET_SIZE = "xl"
DATASET_NAME = f"fma_{DATASET_SIZE}_resampled_{args.sample_rate}_rechanneled_{args.channels}"
DATASET_FOLDER = "../data/audio/"

dataset_path = DATASET_FOLDER + DATASET_NAME

for path, subdirs, files in os.walk(dataset_path):
  
    label = path.split("/")[-1]
    
    if (label in args.genres):
      for name in tqdm(files, colour="cyan", leave=True):
        
        file_audio_path = os.path.join(path, name)
        
        new_file_audio_path = file_audio_path.replace(
          '.mp3', '_rechanneled_resampled.mp3'
        )

        os.system(
          f"ffmpeg -i {file_audio_path} " + 
          f"-ac {args.channels} -ar {args.sample_rate} " + 
          f"-c:a libmp3lame -q:a 0 {new_file_audio_path} " + 
          f"-y -hide_banner -loglevel error"
        ) 
        
        os.system(f"rm -f {file_audio_path}")  
        
        os.system(f"mv -f {new_file_audio_path} {file_audio_path}")
