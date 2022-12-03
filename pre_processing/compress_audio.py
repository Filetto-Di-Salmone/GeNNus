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
args = parser.parse_args()

DATASET_SIZE = "large"
DATASET_NAME = f"fma_{DATASET_SIZE}_organized_by_label_resampled_rechanneled"
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
          f"ffmpeg -i {file_audio_path} -ac 1 -ar 8000 -c:a libmp3lame -q:a 0 {new_file_audio_path} -y -hide_banner -loglevel error"
        ) 
        
        os.system(f"rm -f {file_audio_path}")  
        
        os.system(f"mv -f {new_file_audio_path} {file_audio_path}")
